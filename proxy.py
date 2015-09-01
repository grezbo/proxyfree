__author__ = 'mork'

class Proxy(object):
    def __init__(self, ip, port, type='', describe='', delay=-1):
        self.ip = ip
        self.port = port
        self.type = type
        self.describe = describe
        self.delay = delay

    def print_proxy(self):
        print '%s:%s %s %s %s' % (self.ip, self.port, self.delay, self.type, self.describe)

    def print_proxy_without_delay(self):
        print '%s:%s %s %s' % (self.ip, self.port, self.type, self.describe)

    def print_proxy_simple(self):
        print '%s:%s' % (self.ip, self.port)

