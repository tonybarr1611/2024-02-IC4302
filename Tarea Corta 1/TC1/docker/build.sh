#!/bin/bash
# $1 is the username
docker login
cd FlaskApp
docker build -t $1/flaskapi .
docker push $1/flaskapi
cd ..