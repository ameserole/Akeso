from .. import ServiceFrame
import docker
import urllib2
import structlog

logger = structlog.get_logger()


class ServiceCheck(ServiceFrame.ServiceFrame):
    def __init__(self, serviceInfo):
        ServiceFrame.ServiceFrame.__init__(self, serviceInfo)
        self.flag = "gigem{apache_traversal}"

    def checkService(self):
        url = "http://{}/".format(self.serviceInfo.serviceHost)
        msg = "Attempting to open {}".format(url)
        logger.info("ApacheDirectoryTraversal", msg=msg, serviceInfo=self.serviceInfo)
        try:
            resp = urllib2.urlopen(url).read()
            if resp != "Hello Word\n":
                msg = "Incorrect Response {}".format(resp)
                logger.info("ApacheDirectoryTraversal", msg=msg, serviceInfo=self.serviceInfo.__dict__)
                return False
            msg = "Succesfully open {}: {}".format(url, resp)
            logger.info("ApacheDirectoryTraversal", msg=msg, serviceInfo=self.serviceInfo.__dict__)
            return True
        except: # NOQA
            msg = "Failed to open {}".format(url)
            logger.info("ApacheDirectoryTraversal", msg=msg, serviceInfo=self.serviceInfo.__dict__)
            return False
        return False

    def getLogs(self):
        client = docker.from_env(version="auto")
        container = client.containers.get(self.serviceInfo.serviceName)
        return container.logs()
