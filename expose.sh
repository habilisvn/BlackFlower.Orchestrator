#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Error: Please provide exactly one parameter (1 for Redis, 2 for Kafka, 3 for RabbitMQ, 4 for PostgreSQL)"
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
    3)
        echo "Exposing RabbitMQ service..."
        minikube kubectl port-forward svc/rabbitmq 5672:5672 15672:15672
        ;;
    4)
        echo "Exposing PostgreSQL service..."
        minikube kubectl port-forward svc/postgres 5432:5432
        ;;
    *)
        echo "Error: Invalid parameter. Use 1 for Redis, 2 for Kafka, 3 for RabbitMQ, or 4 for PostgreSQL"
        exit 1
        ;;
esac
