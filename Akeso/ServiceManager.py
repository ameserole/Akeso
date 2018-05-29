
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
        self.exploitModules = info['exploitModules']
        self.serviceCheckNames = info['serviceCheckNames']
        self.userInfo = info['userInfo']
