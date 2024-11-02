#!/bin/bash
helm list
helm uninstall webapp
helm uninstall application
helm uninstall databases
helm uninstall bootstrap