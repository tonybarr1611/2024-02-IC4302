#!/bin/bash
helm list
helm uninstall grafana-config

helm uninstall app

helm uninstall databases

helm uninstall monitoring-stack

helm uninstall bootstrap