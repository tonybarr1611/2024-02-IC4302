#!/bin/bash
cd bootstrap
rm -rf Chart.lock
helm dependency update
cd ..
helm upgrade --install bootstrap bootstrap
sleep 20
cd databases
rm -rf Chart.lock
helm dependency update
cd ..
helm upgrade --install databases databases
sleep 60
helm upgrade --install application application