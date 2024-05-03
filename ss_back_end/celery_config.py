from celery import Celery

app = Celery('ss_back_end', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')

import ss_app.semantic_search
