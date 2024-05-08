#!/bin/bash

# Start RabbitMQ server
rabbitmq-server &

# Start Redis server
redis-server &

# Start Celery
./start-celery-worker.sh &
