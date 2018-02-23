from .. import ServiceFrame
import docker
import requests
import structlog

logger = structlog.get_logger()


class ServiceCheck(ServiceFrame.ServiceFrame):
    def __init__(self, serviceInfo):
        ServiceFrame.ServiceFrame.__init__(self, serviceInfo)
        self.flag = "gigem{can_you_sql_the_problem}"

    def checkService(self):
        url = "http://{}/login.php".format(self.serviceInfo.serviceHost)
        msg = "Attempting to open {}".format(url)
        logger.info("SQLiSimple", msg=msg, serviceInfo=self.serviceInfo.__dict__)
        try:
            data = {'username': 'admin', 'password': '708DxSUf2O%C*pLWNI'}
            r = requests.post(url, data=data)
            if '<html>You logged in as admin</html>' not in r.text:
                msg = "Incorrect Response {}".format(r.text)
                logger.info("SQLiSimple", msg=msg, serviceInfo=self.serviceInfo.__dict__)
                return False
            msg = "Succesfully open {}: {}".format(url, r.text)
            logger.info("SQLiSimple", msg=msg, serviceInfo=self.serviceInfo.__dict__)
            return True

        except: # NOQA
            msg = "Failed to open {}: {}".format(url, data)
            logger.info("SQLiSimple", msg=msg, serviceInfo=self.serviceInfo.__dict__)
            return False
        return False

    def getLogs(self):
        client = docker.from_env(version="auto")
        container = client.containers.get(self.serviceInfo.serviceName)
        tarstream, stat = container.get_archive('/var/log/apache2/error.log')
        return str(tarstream.read())
