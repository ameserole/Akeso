#!/usr/bin/env python

import argparse
import docker
import time
import os
from Akeso import config


def activate_venv():
    # https://www.a2hosting.com/kb/developer-corner/python/activating-a-python-virtual-environment-from-a-script-file
    venv_file = os.path.join(os.getcwd(), 'akeso_venv/bin/activate_this.py')
    if os.path.isfile(venv_file):
        activate_this = venv_file
        execfile(activate_this, dict(__file__=activate_this))  # NOQA


def start_rabbitmq_container():
    client = docker.from_env()
    try:
        rabbit = client.containers.get('shell-rabbit')
    except docker.errors.NotFound:
        client.containers.run(image='rabbitmq:latest', detach=True, hostname='shell-rabbit', name='shell-rabbit')
        time.sleep(10)


def main():
    parser = argparse.ArgumentParser(description="Command Line Interface for Akeso")

    parser.add_argument("-a", "--attack-workers", type=int, help="Number of attack workers to start with. Default is two.")
    parser.add_argument("-d", "--daemon", help="Run in background (not implemented yet)")
    parser.add_argument('-l', '--log-dir', help="Logging Directory (not implemented yet)")

    args = parser.parse_args()

    if args.attack_workers is not None:
        config.NUM_ATTACK_WORKERS = args.attack_workers

    activate_venv()
    start_rabbitmq_container()

    from Akeso import DefenseLab  # NOQA


if __name__ == '__main__':
    main()
