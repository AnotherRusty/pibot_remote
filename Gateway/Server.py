#!/usr/bin/env python

from __future__ import print_function

'''
    threading tcp server
'''

from SocketServer import BaseRequestHandler, ThreadingTCPServer
from Transport import Transport
import threading


class Handler(BaseRequestHandler):
    def handle(self): # handle function must be overrided
        addr = self.client_address
        client = self.request
        print(addr, ' connected')
        transport = Transport(addr, client)
        transport.setDaemon(True)
        transport.start()
        while True:
            pass


class Server(threading.Thread):
    def __init__(self, host=None, port=None):
        threading.Thread.__init__(self)

        self.__host = host
        self.__port = port
    
    def run(self):
        if self.__host is None or self.__port is None:
            print('Please specify the host ip and port.')
            return
        addr = (self.__host, self.__port)
        self.server = ThreadingTCPServer(addr, Handler)
        print('Start TCP server at ', self.__host, ':', self.__port)
        self.server.serve_forever()
        
