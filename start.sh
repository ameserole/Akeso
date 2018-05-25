#!/bin/bash

set -exo pipefail

source akeso_venv/bin/activate

docker run -d --hostname shell-rabbit --name rabbit-server -p 5672:5672 -p 15672:15672 rabbitmq:latest

pushd Akeso/
    python DefenseLab.py 
popd

