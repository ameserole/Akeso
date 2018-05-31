#!/bin/bash

set -exo pipefail

sudo apt update
sudo apt install -y python-pip docker.io

sudo pip install virtualenv

virtualenv akeso_venv
source akeso_venv/bin/activate

pip install -r requirements.txt

if id -nG "$USER" | grep -qw "docker"; then
    echo "User AkesoCLI.py to bring the backend up."
else
    echo "Adding $USER to docker group"
    getent group docker || sudo groupadd docker
    sudo usermod -a -G docker $USER
    echo "Please relogin before starting up Akeso"
    exit
fi

