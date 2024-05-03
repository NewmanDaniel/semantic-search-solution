import pandas as pd
import sys
import torch
from transformers import BertTokenizer, BertModel, logging
import pickle
from torch.nn.functional import cosine_similarity
from tqdm import tqdm  # Importing tqdm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from celery_config import app


# Check for NVIDIA GPU with CUDA, then for Apple Silicon GPU (MPS), otherwise use CPU
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

logging.set_verbosity_error()

# Instantiate the model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = SentenceTransformer('all-mpnet-base-v2').to(device)

BATCH_SIZE = 128

def tokenize_description(description):
    """Tokenizes the proposal description."""
    return tokenizer.tokenize(description)

def filter_out_descriptions_longer_than_512(data):
    """
    Filters out descriptions with more than 512 tokens and saves their IDs to omitted.txt.
    Just does an approximation for now by using split
    """
    data = data.dropna(subset=['DESCRIPTION'])
    descriptions = data['DESCRIPTION'].str.split().str.len()
    mask = descriptions <= 512
    omitted_ids = data.loc[~mask, 'ID']
    omitted_ids.to_csv("omitted.txt", index=False, header=False)
    return data[mask]

def get_embedding(tokens):
    """Returns the BERT embedding for tokenized input."""
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    while len(input_ids) < 512:
        input_ids.append(0)
    attention_mask = [1 if i != 0 else 0 for i in input_ids]

    # Move the model to the MPS device.
    model.to(device)

    # Move the input tensor to the MPS device. -- recommended fix by bard
    input_ids = torch.tensor(input_ids).unsqueeze(0).to(device)
    attention_mask = torch.tensor(attention_mask).unsqueeze(0).to(device)

    with torch.no_grad():
       out = model(input_ids, attention_mask=attention_mask)

    return out[0][0,0,:].cpu().numpy()

def get_embeddings_batch(tokenized_descriptions):
    """Returns the BERT embeddings for a batch of tokenized descriptions."""
    input_ids_list = []
    attention_mask_list = []

    for tokens in tokenized_descriptions:
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        while len(input_ids) < 512:
            input_ids.append(0)
        attention_mask = [1 if i != 0 else 0 for i in input_ids]

        input_ids_list.append(input_ids)
        attention_mask_list.append(attention_mask)

    with torch.no_grad():
        out = model(torch.tensor(input_ids_list), attention_mask=torch.tensor(attention_mask_list))
    return out[0][:,0,:].numpy()

def save_embeddings(data):
    """Saves embeddings for all valid descriptions in batches."""
    embeddings = model.encode(data['DESCRIPTION'].tolist(), convert_to_numpy=True, show_progress_bar=True)
    with open('embeddings_new_model.pkl', 'wb') as f:
        pickle.dump(embeddings, f)

def find_similar_proposals(DESCRIPTION, top_k=5):
    """Finds and returns the indices of the top_k most similar proposal descriptions."""
    embedding = model.encode(DESCRIPTION, convert_to_numpy=True)
    with open('embeddings_new_model.pkl', 'rb') as f:
        saved_embeddings = pickle.load(f)
    similarities = cosine_similarity([embedding], saved_embeddings)
    return similarities.argsort(axis=1)[0, -top_k:][::-1]  # get top k indices in descending order

@app.task
def get_top_k_similar_proposals(DESCRIPTION: str, top_k: int=5) -> list:
    f = open('dbpath.txt', r)
    path = f.read()
    data = pd.read_csv(path)
    # TODO cache or optimize filter_out_descriptions - no reason to repeat this.
    valid_data = filter_out_descriptions_longer_than_512(data)

    similar_proposal_indices = find_similar_proposals(DESCRIPTION, top_k=top_k)
    return [(row[1]['ID'], row[1]['DESCRIPTION']) for row in valid_data.iloc[similar_proposal_indices].iterrows()]

if __name__ == "__main__":
    path = sys.argv[1]
    data = pd.read_csv(path)
    print("- Loaded proposals csv")

    print('- Assigning csv path')
    f = open('dbpath.txt', 'w')
    f.write(path)

    valid_data = filter_out_descriptions_longer_than_512(data)
    print("- Saving embeddings")
    save_embeddings(valid_data)
    print("- Saved embedding data. Training complete!")

    print("- Test Inference: ")
    DESCRIPTION = "derivatives compliance program that does not classify swap derivates"
    similar_proposal_indices = find_similar_proposals(DESCRIPTION, top_k=5)

    # print logic
    results_to_print = [(row[1]['ID'], row[1]['DESCRIPTION']) for row in valid_data.iloc[similar_proposal_indices].iterrows()]
    for i, row in enumerate(results_to_print):
        print(f'{i}: {row}')
