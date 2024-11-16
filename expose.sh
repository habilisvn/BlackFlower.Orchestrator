#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Error: Please provide exactly one parameter (1 for Redis, 2 for Kafka)"
    exit 1
fi

case $1 in
    1)
        echo "Exposing Redis service..."
        minikube kubectl port-forward svc/redis 6379:6379
        ;;
    2)
        echo "Exposing Kafka service..."
        minikube kubectl port-forward svc/kafka 9092:9092
        ;;
    *)
        echo "Error: Invalid parameter. Use 1 for Redis or 2 for Kafka"
        exit 1
        ;;
esac
