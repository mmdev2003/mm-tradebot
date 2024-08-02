#!/bin/bash


apt-get install ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/system.asc
chmod a+r /etc/apt/keyrings/system.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/system.list > /dev/null
apt-get update -y

sudo apt-get install system-ce system-ce-cli containerd.io system-buildx-plugin system-compose-plugin -y