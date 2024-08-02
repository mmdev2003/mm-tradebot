#!/bin/bash

apt update -y
apt upgrade -y

# Запуск контейнеров из system-compose.yml
docker compose -f system/services/docker-compose.yml down
docker compose -f system/services/docker-compose.yml up --build