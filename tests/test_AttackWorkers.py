import mock
import pytest
import json
from Akeso.AttackWorkers import attackCallback # NOQA


@pytest.fixture
def fake_module():
    class Fake_Exploit:
        def __init__(self, exploit_ret):
            self.exploit_ret = exploit_ret

        def exploit(self):
            pass

        def exploitSuccess(self):
            return self.exploit_ret

    class Fake_Check:
        def __init__(self, service_ret):
            self.service_ret = service_ret
            self.flag = "flag"

        def checkService(self):
            return self.service_ret

        def getLogs(self):
            return "logs"

    class module:
        def __init__(self, service_ret, exploit_ret):
            self.service_ret = service_ret
            self.exploit_ret = exploit_ret
            self.flag = "flag"

        def ServiceCheck(self, service):
            return Fake_Check(self.service_ret)

        def Exploit(self, service):
            return Fake_Exploit(self.exploit_ret)

    return module


@pytest.mark.parametrize("service_ret, exploit_ret, expected_message", [
    (True, True, {'msg': 'Your Code/Config was exploited.', 'display': 'msg'}),
    (True, False, {'msg': 'Service Check Succeeded After Attack', 'flag': 'flag', 'display': 'flag'}),
    (False, True, {'msg': 'Service Check Failed', 'logs': 'logs', 'display': 'logs'}),
    (False, False, {'msg': 'Service Check Failed', 'logs': 'logs', 'display': 'logs'})
])
def test_attackCallback(service_ret, exploit_ret, expected_message, fake_ch, fake_method, fake_service, fake_module):
    with mock.patch('pika.channel.Channel.basic_publish') as pikaPub, \
            mock.patch('importlib.import_module') as importMod:#, \
#            mock.patch('Akeso.AttackWorkers.cleanup') as fakeClean:
        pikaPub.return_value = None
        importMod.return_value = fake_module(service_ret, exploit_ret)
#        fakeClean.return_value = None

        ch = fake_ch
        method = fake_method
        properties = ""
        body = json.dumps(fake_service.__dict__)
        expected_message['service'] = fake_service.__dict__
        attackCallback(ch, method, properties, body)

        pikaPub.assert_called_with(exchange='resultX',
                                   routing_key=str(fake_service.userInfo),
                                   body=json.dumps(expected_message),
                                   immediate=False,
                                   mandatory=False,
                                   properties=None)
        print expected_message
