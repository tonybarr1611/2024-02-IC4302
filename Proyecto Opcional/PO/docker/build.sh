#!/bin/bash
# $1 is the username
docker login
cd downloader
docker build -t $1/downloader .
docker push $1/downloader

cd ../s3-spider

docker build -t $1/s3-spider .
docker push $1/s3-spider

cd ../spark-job

docker build -t $1/spark-job .
docker push $1/spark-job