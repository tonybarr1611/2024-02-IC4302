#!/bin/bash
# $1 is the username
docker login

cd backend-api
docker build -t $1/backend-api .
docker push $1/backend-api

cd ../backend-api-memcached
docker build -t $1/backend-api-memcached .
docker push $1/backend-api-memcached

cd ../frontend
docker build -t $1/frontend .
docker push $1/frontend

cd ../huggingface-api
docker build -t $1/huggingface-api .
docker push $1/huggingface-api

cd ./ingest
docker build -t $1/ingest .
docker push $1/ingest

cd ../s3-crawler
docker build -t $1/s3-crawler .
docker push $1/s3-crawler