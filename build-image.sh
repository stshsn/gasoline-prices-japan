#!/bin/bash

GIT_COMMIT_ID=$(git rev-parse HEAD)
GIT_SHORT_COMMIT_ID=$(git rev-parse --short HEAD)
IMAGE_NAME=gasoline-prices:${GIT_SHORT_COMMIT_ID}

docker image inspect ${IMAGE_NAME} >& /dev/null
if [ $? -eq 0 ]; then
    echo "WARNING: ${IMAGE_NAME} is already exist."
    echo "If you want to remove this, run following command."
    echo "    docker image rm ${IMAGE_NAME}"
    exit 1
fi

docker build --build-arg GIT_COMMIT_ID=${GIT_COMMIT_ID} -t ${IMAGE_NAME} -f docker/Dockerfile .
