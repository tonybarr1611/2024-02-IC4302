#!/bin/bash

# Function to replace files based on user input
replace_files() {
    local directory=$1
    local file1=$2

    # Check if the file exists before replacing
    if [[ -f $file1 ]]; then
        # Replace the file (move new ones in place)
        cp -f "$file1" "$directory"
        echo "Files replaced successfully in $directory"
    else
        echo "File does not exist: $file1"
    fi
}

# Function to update and upgrade Helm charts
update_helm_charts() {
    local chart=$1

    cd "$chart" || exit
    rm -rf Chart.lock
    helm dependency update
    cd ..
    helm upgrade --install "$chart" "$chart"
}

# Asking for user input
while true; do
    echo "Please choose an option:"
    echo "1. With Cache"
    echo "2. Without Cache"
    read -p "Enter your choice (1 or 2): " choice

    # Navigate to CacheTemp directory
    cd ../../CacheTemp || exit

    case $choice in
        1)
            cd UsesCache
            # Replace files for option 1
            replace_files "../../P1/charts/webapp" "./webapp/values.yaml"
            replace_files "../../P1/charts/grafana-config" "./grafana-config/values.yaml"
            replace_files "../../P1/charts/grafana-config/dashboards" "./grafana-config/dashboards/backendapicached.json"
            ;;
        2)
            cd NoCache
            # Replace files for option 2
            replace_files "../../P1/charts/webapp" "./webapp/values.yaml"
            replace_files "../../P1/charts/grafana-config" "./grafana-config/values.yaml"
            replace_files "../../P1/charts/grafana-config/dashboards" "./grafana-config/dashboards/backendapi.json"
            ;;
        *)
            echo "Invalid choice. Please enter either 1 or 2."
            continue
            ;;
    esac

    # Ask if the user wants to continue with the Helm updates
    read -p "Do you want to continue with Helm updates? (y/n): " continue_choice
    if [[ "$continue_choice" != "y" ]]; then
        break
    fi

    # Navigate to the charts directory and update Helm charts
    cd "../../P1/charts" || exit

    # Update and upgrade all required charts
    update_helm_charts "bootstrap"
    update_helm_charts "monitoring-stack"
    update_helm_charts "databases"
    update_helm_charts "application"
    update_helm_charts "webapp"
    update_helm_charts "grafana-config"

    # Break the loop after completion
    break
done
