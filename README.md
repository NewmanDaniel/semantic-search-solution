# Semantic Search Solution
Are you struggling to find relevant items in your text database using standard keyword searches? 
Do you often have a general idea of what you're looking for, but fail to find the right results?
This full "semantic search" solution may be just what you need.

Leveraging BERT, With Semantic Search Solution you can perform high quality semantic searches on your dataset using your own personal hardware.
```
For example: a feedback coordinator is tasked with managing tens of thousands of feedback items. One of her responsibilities is
merging incoming duplicate entries to items already in the database. The feedback coordinator performs a semantic search query:

"After an audit of our access submodules, we've revealed some outstanding exploits that can be leveraged to access secret items."
Then, the top k most similar results are returned:

FCITEM-61: There are critical flaws in our access control systems, allowing unauthorized access to sensitive compliance data. Overhaul of security protocols is needed.
FCITEM-20: Recent breaches highlight weaknesses in our data security framework. Propose an immediate security audit and enhancements.
FCITEM-8: Inconsistent application of security protocols across platforms observed. Requires standardization and rigorous testing.  
...
```

*Semantic Search Solution* is:
* High quality: thanks to the underlying well-trained BERT model, has excellent semantic matching capabilities to find the data you need, when you need it.
* Easy: Simple to use and deploy. Get this running on your dataset within 20 minutes, then expose search functionality with a friendly UI.
* Private: No internet connectivity is needed. Keep your data safe and confidential within your organization.
* Fast: Leverages your Nvidia GPU or Macbook Metal for fast searches, even with 10s of thousands of items

# initial setup
_Note: Python 3.11.2 has been tested_
1. setup virtualenv: virtualenv -ppython3 venv 
2. install requirements: pip install -r requirements.txt
3. cd ss_back_end (please remain in this directory for all backend commands)
4. run this command: rabbitmq-server (have to manually start this on mac, you may have a service to start on linux)
5. run start *celery worker start-celery-worker.sh* in a seperate tab
_You must ensure that celery and rabbitmq-server are running to use the full system_

# completely train a model and run a test semantic search 
```
python -m ss_app.semantic_search 'sample_data/financial_compliance_feedback_database.csv'
```
When the command is completed, a test inference will run.
_note: if this step takes more than a few seconds, the software didn't detect nvidia or macbook hardware and is using the CPU_

# test inference via task system
perform this step to ensure that the task queueing system is functional before starting API server
```
python -m ss_app.main
```

# start API server
python manage.py runserver 127.0.0.1:7878

# setup and start frontend
1. navigate to front-end/
2. cp config.js.example config.js , and configure your hostname
3. open index.html in your browser. You should be able to submit requests to the API

# I want to use my own data!
Please construct a CSV with the following header:
```
"ID","TITLE","DESCRIPTION"
"FCITEM-1","Glitch in Transaction Flagging","The system incorrectly flags legitimate transactions as suspicious. Requires urgent review of the flagging algorithms to reduce false positives."
"FCITEM-2","Dashboard Usability Enhancement","Users report difficulty navigating the dashboard, especially finding specific compliance reports. Suggest redesigning the UI for easier access."
...
```
then, repeat 
```
python -m ss_app.semantic_search 'sample_data/financial_compliance_feedback_database.csv'
```
and replace path with the path of your CSV.

