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

cd FlaskAppMariaDB
docker build -t $1/flaskapimariadb .
docker push $1/flaskapimariadb
cd ..

cd FlaskAppElasticSearch
docker build -t $1/flaskapies .
docker push $1/flaskapies
cd ..

cd FlaskAppMariaDBMemcached
docker build -t $1/flaskapimariadbmemcached .
docker push $1/flaskapimariadbmemcached
cd ..

cd loader
docker build -t $1/loader .
docker push $1/loader
cd ..