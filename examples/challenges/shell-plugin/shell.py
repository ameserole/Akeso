from .. import ServiceFrame
from string import ascii_letters
import docker
import structlog
import requests
import sys
import random
import paramiko
from time import sleep

logger = structlog.get_logger()


class ServiceCheck(ServiceFrame.ServiceFrame):
    def __init__(self, serviceInfo):
        ServiceFrame.ServiceFrame.__init__(self, serviceInfo)
        self.flag = "gigem{1nj3ct_r3j3ct_67c9411}"

    def checkService(self):
        url = "http://{}:4001/register".format(self.serviceInfo.serviceHost)

        msg = "Attempting to open {}".format(url)
        logger.info("Shell", msg=msg, serviceInfo=self.serviceInfo.__dict__)

#        try:
        name = ''.join(random.choice(ascii_letters) for i in range(16))
        s = requests.Session()
        r = s.get(url)
        snum = r.text.find('type="hidden" name="nonce" value="')
        nonce = r.text[snum+34:snum+34+128]
        payload = (('name', name),('email', name + '@a.com'),('password', 'asdf'), ('nonce', nonce))
        r = s.post(url, data=payload)
        if r.status_code != 200:
            msg = "Incorrect Response {}".format(r.status_code)
            logger.info("Shell", msg=msg, serviceInfo=self.serviceInfo.__dict__)
            return False

        msg = "Succesfully registered {}: {}".format(url, r.status_code)
        logger.info("Maze", msg=msg, serviceInfo=self.serviceInfo.__dict__)
    
        sleep(1)

#        sleep(60)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.serviceInfo.serviceHost, username=name, password='asdf')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('whoami', get_pty=True)
       
        if ssh_stdout.read().decode('ascii').strip() != name:
            msg = "Incorrect Response {} {}".format(ssh_stdout.read().decode('ascii'), ssh_stderr.read().decode('ascii'))
            logger.info("Shell", msg=msg, serviceInfo=self.serviceInfo.__dict__)
            return False


        msg = "Succesfully logged in {}: {}".format(url, name)
        logger.info("Shell", msg=msg, serviceInfo=self.serviceInfo.__dict__)
        return True
        

#        except: # NOQA
#            exception = sys.exc_info()[0]
#            msg = "Failed to open {} Exception {}".format(url, exception)
#            logger.info("Shell", msg=msg, serviceInfo=self.serviceInfo.__dict__)
#            return False      
        return False

    def getLogs(self):
        client = docker.from_env(version="auto")
        container = client.containers.get(self.serviceInfo.serviceName)
        tarstream, stat = container.get_archive('/logs.txt')
        return str(tarstream.read())      

            
