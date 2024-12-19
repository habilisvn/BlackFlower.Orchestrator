#!/bin/bash

# Build Docker image
echo "Building Docker image..."
docker build -t habilisv/fastapi:1.0 .

# Push Docker image to Docker Hub
echo "Pushing Docker image to Docker Hub..."
docker push habilisv/fastapi:1.0

# Enable Ingress addon for Minikube
echo "Enabling Ingress addon for Minikube..."
minikube addons enable ingress

# Apply Kubernetes configuration
echo "Applying Kubernetes configuration..."
minikube kubectl -- apply -f kubernetes/fastapi.yaml
minikube kubectl -- apply -f kubernetes/ingress.yaml

# Rollout restart FastAPI deployment
echo "Restarting FastAPI deployment..."
minikube kubectl rollout restart deployment fastapi

echo "Deployment complete!"
