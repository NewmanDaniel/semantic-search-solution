#!/bin/bash

# Start RabbitMQ server
rabbitmq-server &

# Start Redis server
redis-server &

# Start Celery
./start-celery-worker.sh &

# start web server
python manage.py runserver 0.0.0.0:7878
