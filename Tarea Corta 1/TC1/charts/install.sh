#!/bin/bash
cd bootstrap
rm -rf Chart.lock
rm -rf charts
helm dependency update
cd ..
helm upgrade --install bootstrap bootstrap
sleep 20


cd monitoring-stack
rm -rf Chart.lock
rm -rf charts
helm dependency update
cd ..
helm upgrade --install monitoring-stack monitoring-stack
sleep 20

cd databases
rm -rf Chart.lock
rm -rf charts
helm dependency update
cd ..
helm upgrade --install databases databases
sleep 60

helm upgrade --install app app
sleep 20

cd grafana-config
rm -rf Chart.lock
rm -rf charts
helm dependency update
cd ..
helm upgrade --install grafana-config grafana-config
