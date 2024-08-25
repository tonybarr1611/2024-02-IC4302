#!/bin/bash
helm list
helm uninstall grafana-config
sleep 15
helm uninstall app
sleep 15
helm uninstall databases
sleep 40
helm uninstall monitoring-stack
sleep 60
helm uninstall bootstrap