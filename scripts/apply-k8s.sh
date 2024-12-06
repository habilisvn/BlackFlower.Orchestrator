#!/bin/bash

# Set the directory containing kubernetes yaml files
K8S_DIR="../kubernetes"

# Check if the directory exists
if [ ! -d "$K8S_DIR" ]; then
    echo "Error: Directory $K8S_DIR not found!"
    exit 1
fi

# Print information
echo "Applying Kubernetes configurations from $K8S_DIR"
echo "-------------------------------------------"

# Find and apply all yaml files
for file in "$K8S_DIR"/*.{yaml,yml}; do
    if [ -f "$file" ]; then
        echo "Applying $file..."
        kubectl apply -f "$file"
        echo "-------------------------------------------"
    fi
done

echo "Completed applying Kubernetes configurations!"