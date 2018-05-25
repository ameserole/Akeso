from .. import ServiceFrame
import docker
import structlog
import urllib2
import sys

logger = structlog.get_logger()


class ServiceCheck(ServiceFrame.ServiceFrame):
    def __init__(self, serviceInfo):
        ServiceFrame.ServiceFrame.__init__(self, serviceInfo)
        self.flag = "gigem{maze}"

    def checkService(self):
        url = "http://{}:31337/".format(self.serviceInfo.serviceHost)
        msg = "Attempting to open {}".format(url)
        logger.info("Maze", msg=msg, serviceInfo=self.serviceInfo.__dict__)
        startString = '<html>\n<head>\n        <meta charset="UTF-8" />\n        <title>Maze Problem</title>\n        <script src="//cdn.jsdelivr.net/phaser/2.6.2/phaser.min.js"></script>\n                <script src="http://cdn.socket.io/socket.io-1.4.5.js"></script>\n</head>\n<body>\n\n'

        try:
            response = urllib2.urlopen(url)
            r = response.read()
            logger.info("Maze", msg=r)
            if not r.startswith(startString):
                msg = "Incorrect Response {}".format(r)
                logger.info("Maze", msg=msg, serviceInfo=self.serviceInfo.__dict__)
                return False
            msg = "Succesfully opened {}: {}".format(url, r)
            logger.info("Maze", msg=msg, serviceInfo=self.serviceInfo.__dict__)
            return True

        except: # NOQA
            exception = sys.exc_info()[0]
            msg = "Failed to open {}\nException {}".format(url, exception)
            logger.info("Maze", msg=msg, serviceInfo=self.serviceInfo.__dict__)
            return False
        return False

    def getLogs(self):
        client = docker.from_env(version="auto")
        container = client.containers.get(self.serviceInfo.serviceName)
        tarstream, stat = container.get_archive('/logs.txt')
        return str(tarstream.read())
