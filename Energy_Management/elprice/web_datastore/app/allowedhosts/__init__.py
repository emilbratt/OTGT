
class HostFilter:

    '''
        pass host through any method to check against the
        host stored in configuration/environment
        if match, return True
    '''

    def __init__(self, envar_get: object):
        self.envar_get = envar_get

    def elspot(self, host: str) -> bool:
        return host == self.envar_get('HOST_ELSPOT')

    def plot(self, host: str) -> bool:
        return host == self.envar_get('HOST_PLOT')

    def sensor(self, host: str) -> bool:
        return host == self.envar_get('HOST_SENSOR')

    def test(self, host: str) -> bool:
        print('request from host: ', host)
        return True
