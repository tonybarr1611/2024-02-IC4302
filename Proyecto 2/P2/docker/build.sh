#!/bin/bash
# $1 is the username
docker login

build_docker_image() {
    local image=$1
    cd "$image" || exit
    docker build -t "$2/$image" .
    docker push "$2/$image"
    cd ..
}

build_docker_image "backendStayTune" "$1"
build_docker_image "frontendStayTune" "$1"
build_docker_image "loader" "$1"
build_docker_image "migrator" "$1"