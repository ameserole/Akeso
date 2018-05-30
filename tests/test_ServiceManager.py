from Akeso.ServiceManager import ServiceInfo


def test_ServiceInfo():
    fakeInfo = {
        'serviceName': 'fakeName',
        'imageName': 'fakeImage',
        'serviceHost': '127.0.0.1',
        'servicePort': 80,
        'exploitModules': ['fakeExploit'],
        'serviceCheckNames': ['fakeCheck'],
        'userInfo': 'fakeInfo'}

    service = ServiceInfo(fakeInfo)
    assert service.__dict__ == fakeInfo
