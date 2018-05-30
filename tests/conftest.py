import pytest
from Akeso.ServiceManager import ServiceInfo


@pytest.fixture
def fake_service():
    fakeInfo = {
        'serviceName': 'fakeName',
        'imageName': 'fakeImage',
        'volumeLocation': 'fakeVolume',
        'serviceHost': '127.0.0.1',
        'servicePort': 80,
        'exploitModules': ['fakeExploit'],
        'serviceCheckNames': ['fakeCheck'],
        'userInfo': '1'}

    return ServiceInfo(fakeInfo)


@pytest.fixture
def fake_ch():
    class ch:
        def basic_ack(self, delivery_tag=None):
            pass

    return ch()


@pytest.fixture
def fake_method():
    class method:
        delivery_tag = None

    return method()


@pytest.fixture
def fake_container():
    class container():
        def start(self):
            pass

        def logs(self, stdout, stderr):
            return 'logs'

        def stop(self):
            pass

        def remove(self):
            pass

    return container()


@pytest.fixture
def fake_blocking_conn():
    class blocking_conn:
        def channel(self):
            pass

    return blocking_conn()
