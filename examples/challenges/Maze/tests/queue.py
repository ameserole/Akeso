import pika
import json
import sys
import os
import socket
import binascii

def callback(ch, method, properties, body):
    print body
    ch.basic_ack(delivery_tag = method.delivery_tag)
    sys.exit()
    return


info = ('maze', 'mazeAttack', 'maze', 31337)
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.17.0.2')

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='attackQueue', durable=True)


userinfo = binascii.hexlify(os.urandom(32)).decode('ascii')

#Stupid hack I found to get host ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
hostname = s.getsockname()[0]
print(hostname)
s.close()

# A lot of this I won't need anymore
service = {
    'serviceName': 'dontneed',
    'imageName': info[0],
    'volumeLocation': '/fake/path',
    'userInfo': userinfo,
    'exploitModule': info[1],
    'serviceCheckName': info[2],
    'serviceHost': hostname,
    'servicePort': info[3]
}

print "Pushing: {}".format(service)
channel.basic_publish(exchange='',
                      routing_key='attackQueue',
                      body=json.dumps(service))


connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2'))
userChannel = connection.channel()
userChannel.exchange_declare(exchange='resultX')
userChannel.queue_declare(queue='resultQueue', durable=True)


userChannel.queue_bind(exchange='resultX',
                       queue='resultQueue',
                       routing_key=userinfo)

userChannel.basic_consume(callback, queue='resultQueue' )
userChannel.start_consuming()

userChannel.close()

