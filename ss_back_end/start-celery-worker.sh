# be sure to execute `rabbitmq-server-start`
# celery -A celery_config worker --loglevel=info
# NOTE THE BELOW: WE NEED CELERY TO START ON A SINGLE THREAD.
# This is fine: we don't want multiple threads competing for the GPU anyway.
celery -A celery_config worker -P solo -l info
