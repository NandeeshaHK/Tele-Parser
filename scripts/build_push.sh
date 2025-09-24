#!/usr/bin/env bash
IMAGE_NAME=${1:-telemetry-pipeline:latest}
docker build -t $IMAGE_NAME .
# optionally push: docker push $IMAGE_NAME
echo "Built $IMAGE_NAME"
