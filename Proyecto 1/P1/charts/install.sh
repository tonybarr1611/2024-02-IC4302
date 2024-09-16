#!/bin/bash
cd bootstrap
rm -rf Chart.lock
helm dependency update
cd ..
helm upgrade --install bootstrap bootstrap

cd monitoring-stack
rm -rf Chart.lock
helm dependency update
cd ..
helm upgrade --install monitoring-stack monitoring-stack

cd databases
rm -rf Chart.lock
helm dependency update
cd ..
helm upgrade --install databases databases

cd application
rm -rf Chart.lock
helm dependency update
cd ..
helm upgrade --install application application

cd webapp
rm -rf Chart.lock
helm dependency update
cd ..
helm upgrade --install webapp webapp

cd grafana-config
rm -rf Chart.lock
helm dependency update
cd ..
helm upgrade --install grafana-config grafana-config