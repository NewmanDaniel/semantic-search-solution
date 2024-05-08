#!/bin/bash

# Start services
./start-services.sh &
#
# start web server
python manage.py runserver 0.0.0.0:7878
