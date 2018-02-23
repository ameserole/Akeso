
class ServiceFrame(object):
    def __init__(self, serviceInfo):
        self.serviceInfo = serviceInfo
        self.flag = None

    def checkService(self):
        raise NotImplementedError()

    def getLogs(self):
        raise NotImplementedError()
