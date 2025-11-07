#!/bin/bash
# Script para iniciar serviços

echo "Iniciando serviços..."

# Iniciar serviços com Docker Compose
docker-compose up -d

echo "Aguardando serviços iniciarem..."
sleep 10

echo "Serviços iniciados!"
echo "Kafka UI: http://localhost:8081"
echo "Airflow: http://localhost:8080"
echo "MLflow: http://localhost:5000"
echo "Grafana: http://localhost:3000"
echo "Prometheus: http://localhost:9090"
echo "API: http://localhost:8000"

