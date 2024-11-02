#!/bin/bash
kubectl create secret generic gcs-key-secret --from-file=key.json=./secret.json

update_helm_charts() {
    local chart=$1

    cd "$chart" || exit
    rm -rf Chart.lock
    helm dependency update
    cd ..
    helm upgrade --install "$chart" "$chart"
}

update_helm_charts "bootstrap"
update_helm_charts "databases"
sleep 40
update_helm_charts "application"
update_helm_charts "webapp"