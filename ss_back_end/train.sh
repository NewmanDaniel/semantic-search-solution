# Find and replace the line in the settings.py file
# RUN sed -i 's|MODEL_PATH = "./embeddings_new_model.pkl"|MODEL_PATH = "/data/model.pkl"|g' ./ss_back_end/settings.py
sed -i '/^MODEL_PATH/c\MODEL_PATH = "/data/model.pkl"' ./ss_back_end/settings.py

python -m ss_app.semantic_search $1
