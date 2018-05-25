import importlib
import json
import structlog
import pika
import config
from multiprocessing import Process
from ServiceManager import ServiceInfo

logger = structlog.get_logger()


def challenge_mapper(challenge):
    return {
        'maze': ('maze', 'mazeAttack', 'maze', 31337),
        'SQL': ('sqlisimple', 'SQLi', 'SQLiSimple', 80),
        'shell': ('shell', 'shellAttack', 'shell', 4001),
    }[challenge]


def attackCallback(ch, method, properties, body):
    """Pull service off of attack queue and run selected attack against it"""

    connection2 = pika.BlockingConnection(pika.ConnectionParameters(config.RABBITMQ_SERVER))
    resultChannel = connection2.channel()
    resultChannel.exchange_declare(exchange='resultX', exchange_type='direct')
    resultChannel.queue_declare(queue='resultQueue', durable=True)

    body = json.loads(body)
    info = challenge_mapper(body['chal'])

    if 'serviceName' in body:
        serviceName = body['serviceName']
    else:
        serviceName = None

    s = {
        'serviceName': serviceName,
        'imageName': info[0],
        'userInfo': body['userInfo'],
        'exploitModule': info[1],
        'serviceCheckName': info[2],
        'serviceHost': body['serviceHost'],
        'servicePort': info[3]
    }

    logger.info("attackCallback", msg="Recieved Message", body=body)
    service = ServiceInfo(s)

    # Queue for users to reviece the results
    resultChannel.queue_bind(exchange='resultX', queue='resultQueue', routing_key=str(service.userInfo))

    log = logger.bind(service=service.__dict__)
    userMsg = "Starting Attack on {} {}\n".format(service.imageName, service.userInfo)

    # Get the Service module for this service and check that it is running correctly
    serviceCheckModuleName = 'Services.' + service.serviceCheckName + '.' + service.serviceCheckName
    serviceModule = importlib.import_module(serviceCheckModuleName, package=None)
    serviceCheckObject = serviceModule.ServiceCheck(service)

    if serviceCheckObject.checkService():
        log.info('attackCallback', msg="Service Check Succeeded")
        userMsg = "Service Check Succeeded"
    else:
        log.info('attackCallback', msg="Service Check Failed")
        userMsg = "Service Check Failed"
        resultChannel.basic_publish(exchange='resultX',
                                    routing_key=str(service.userInfo),
                                    body=json.dumps({'msg': userMsg, 'service': service.__dict__}))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return -1

    # If the service is running correctly grab the selected exploit module and run it against the current service
    exploitModuleName = 'Exploits.' + service.exploitModule
    exploitModule = importlib.import_module(exploitModuleName, package=None)
    exploitObject = exploitModule.Exploit(service)
    exploitObject.exploit()

    exploitSuccess = exploitObject.exploitSuccess()

    if exploitSuccess:
        userMsg = "Your Code/Config was exploited."
        log.info("attackCallback", msg="Exploit Success")
        resultChannel.basic_publish(exchange='resultX',
                                    routing_key=str(service.userInfo),
                                    body=json.dumps({'msg': userMsg, 'service': service.__dict__}))

        ch.basic_ack(delivery_tag=method.delivery_tag)
        return -1

    else:
        userMsg = "Attack Failed"
        log.info("attackCallback", msg=userMsg)

    # Check to see if the service is still up after the exploit was run
    checkService = serviceCheckObject.checkService()

    # If Service is still up and exploit did not work return the flag to the user
    if not exploitSuccess and checkService:
        log.info('attackCallback', msg="Service Check Succeeded After Attack")
        userMsg = "Service Check Succeeded After Attack\nflag: {}".format(serviceCheckObject.flag)
        resultChannel.basic_publish(exchange='resultX',
                                    routing_key=str(service.userInfo),
                                    body=json.dumps({'msg': userMsg, 'service': service.__dict__}))

    # No flag for you :(
    elif not exploitSuccess and not checkService:
        log.info('attackCallback', msg="Service Check Failed After Attack")
        userMsg = "Service Check Failed After Attack"
        resultChannel.basic_publish(exchange='resultX',
                                    routing_key=str(service.userInfo),
                                    body=json.dumps({'msg': userMsg, 'service': service.__dict__}))

        ch.basic_ack(delivery_tag=method.delivery_tag)
        return -1

    ch.basic_ack(delivery_tag=method.delivery_tag)
    return 1


def attackWorker():
    """Declare attack queue and callback function"""
#    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(config.RABBITMQ_SERVER)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='attackQueue', durable=True)
    logger.info("attackWorker", msg="Starting Attack Worker", queue="attackQueue")
    channel.basic_consume(attackCallback, queue='attackQueue')
    channel.start_consuming()


def startAttackWorkers(numThreads):
    """Start up numThreads attack workers"""
    for i in range(numThreads):
        t = Process(target=attackWorker)
        t.daemon = True
        t.start()
