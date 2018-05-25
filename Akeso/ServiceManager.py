
class ServiceInfo(object):
    """Object to hold information pertaining to each service"""

    def __init__(self, info):
        if 'serviceName' in info:
            self.serviceName = info['serviceName']
        else:
            self.serviceName = None
        self.imageName = info['imageName']
        self.serviceHost = info['serviceHost']
        self.servicePort = info['servicePort']
        self.exploitModule = info['exploitModule']
        self.serviceCheckName = info['serviceCheckName']
        self.userInfo = info['userInfo']
