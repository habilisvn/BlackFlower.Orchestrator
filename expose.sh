#!/bin/bash

echo "Exposing Redis service..."
minikube kubectl port-forward svc/redis 6379:6379 &

echo "Exposing Kafka service..."
minikube kubectl port-forward svc/kafka 9092:9092 &

echo "Exposing RabbitMQ service..."
minikube kubectl port-forward svc/rabbitmq 5672:5672 15672:15672 &

echo "Exposing PostgreSQL service..."
minikube kubectl port-forward svc/postgres 5432:5432 &

wait
