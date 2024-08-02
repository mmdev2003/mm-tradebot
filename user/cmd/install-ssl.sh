#!/bin/bash

apt update -y
apt upgrade -y
source .env
echo "root: $ROOT_PATH"

# Установка docker
# /root/mm-tradebot/system/cmd/install-docker.sh


# Введите по очереди:
# 1) docker compose -f /root/mm-tradebot/system/services/docker-compose-init.yml up -d --build
# 2) docker exec -it nginx sh
# 3) apk add --update python3 py3-pip && apk add certbot && pip install certbot-nginx --break-system-packages && certbot --nginx
# 4) exit
# 5) docker compose -f /root/mm-tradebot/system/services/docker-compose-init.yml down

# SSL выпущен