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
sleep 90

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

# kubectl expose backend-api-service with Port Forwarding from port 32000 to 31000
sleep 60
# Restart the port-forwarding if it fails
kubectl port-forward svc/backend-api-service 31000:5000