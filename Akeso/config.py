import os

# Number of attack workers pulling from the RabbitMQ server
NUM_ATTACK_WORKERS = 2

# Path to the folder containing all of the services
SERVICE_PATH = os.path.join(os.getcwd(), 'Services/')

# Address of the RabbitMQ server
RABBITMQ_SERVER = '172.17.0.2'


def challenge_mapper(challenge):
    return {
        'maze': ('maze', ['mazeAttack'], ['maze'], 31337),
        'SQL': ('sqlisimple', ['SQLi'], ['SQLiSimple'], 80),
        'shell': ('shell', ['shellAttack'], ['shell'], 4001),
        'nginx': ('nginx', ['DirectoryTraversal'], ['ApacheDirectoryTraversal'], 80)
    }[challenge]
