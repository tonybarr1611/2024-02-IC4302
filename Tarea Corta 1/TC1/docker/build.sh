#!/bin/bash
# $1 is the username
docker login
cd FlaskApp
docker build -t $1/flaskapi .
docker push $1/flaskapi
cd ..
cd FlaskAppPostgreSQL
docker build -t $1/flaskapipostgresql .
docker push $1/flaskapipostgresql
cd ..
cd loader
docker build -t $1/loader .
docker push $1/loader
cd ..