#!/bin/bash
cd bootstrap
rm -rf Chart.lock
rm -rf charts
helm dependency update
cd ..
helm upgrade --install bootstrap bootstrap


cd monitoring-stack
rm -rf Chart.lock
rm -rf charts
helm dependency update
cd ..
helm upgrade --install monitoring-stack monitoring-stack

cd databases
rm -rf Chart.lock
rm -rf charts
helm dependency update
cd ..
helm upgrade --install databases databases

helm upgrade --install app app

cd grafana-config
rm -rf Chart.lock
rm -rf charts
helm dependency update
cd ..
helm upgrade --install grafana-config grafana-config
