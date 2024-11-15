#!/bin/bash

# This script will start all containers defined in docker-compose.yml
echo "Updating minikube deployment and services..."
kubectl apply -f deployment.yaml