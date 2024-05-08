# build image
This step takes a while on first run
```
sudo docker compose build
```

# ingest image

# run image
```
sudo docker compose up
```

# Train using your own csv
1. get the name of the currently run docker with docker compose ps
2. replace the name of the docker in the below command
3. run:
```
sudo docker exec -it semantic-search-solution-semanticsearch-1 /bin/bash ./train.sh /data/yourdata.csv
```
