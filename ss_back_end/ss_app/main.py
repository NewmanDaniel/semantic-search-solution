"""
Sets up celery task and wraps get_top_k_similar_proposals with it
"""
from time import sleep

from ss_app.semantic_search import get_top_k_similar_proposals
from celery_config import app

description = "i cant enter data into some fields for complianace, like its trying to validate the data but can't"

results = get_top_k_similar_proposals.delay(description, 10)

results = results.get()
print(results)
