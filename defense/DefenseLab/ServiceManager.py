import docker
import structlog
import time

logger = structlog.get_logger()

client = docker.from_env(version="auto")


class ServiceInfo(object):
    """Object to hold information pertaining to each service"""

    def __init__(self, info):
        try:
            self.serviceName = info['serviceName']
        except:
            self.serviceName = None
        self.imageName = info['imageName']
        self.serviceHost = info['serviceHost']
        self.servicePort = info['servicePort']
        self.exploitModule = info['exploitModule']
        self.serviceCheckName = info['serviceCheckName']
        self.userInfo = info['userInfo']

