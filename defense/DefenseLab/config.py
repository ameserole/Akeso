import os

# Number of attack workers pulling from the RabbitMQ server
NUM_ATTACK_WORKERS = 2

# Path to the folder containing all of the services
SERVICE_PATH = os.path.join(os.getcwd(), 'Services/')

# Address of the RabbitMQ server
RABBITMQ_SERVER = '172.17.0.2'
