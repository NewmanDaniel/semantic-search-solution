# build image
This step takes a while on first run
```
sudo docker compose build
```

# run image
```
sudo docker compose up
```
You should then be able to use this the same way with running python manage.py runserver directly, follow the other readme.

# Train using your own csv
1. get the name of the currently run docker with docker compose ps
2. replace the name of the docker in the below command
3. run:
```
sudo docker exec -it semantic-search-solution-semanticsearch-1 /bin/bash ./train.sh /data/yourdata.csv
```
