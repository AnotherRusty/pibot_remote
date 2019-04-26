#!/usr/bin/env python

'''
    threading tcp server
'''
import sys
sys.path.append("..")
import pypibot
from pypibot import log
from SocketServer import BaseRequestHandler, ThreadingTCPServer
from Transport import Transport
import threading
from time import sleep


class Handler(BaseRequestHandler):
    __CHECK_CONNECTION_INTERVAL = 5 # seconds

    def handle(self): # handle function must be overrided
        addr = self.client_address
        client = self.request
        log.i('%s connected'%str(addr))
        transport = Transport(addr, client)
        transport.setDaemon(True)
        transport.start()
        while True:
            if not transport.check_status():
                transport.shutdown()
                client.close()
                log.w('%s disconnected'%str(addr))
                break
            sleep(self.__CHECK_CONNECTION_INTERVAL)
            

class Server(threading.Thread):
    def __init__(self, host=None, port=None):
        threading.Thread.__init__(self)

        self.__host = host
        self.__port = port
    
        addr = (self.__host, self.__port)
        self.server = ThreadingTCPServer(addr, Handler)
    def run(self):
        if self.__host is None or self.__port is None:
            log.err('Please specify the host ip and port.')
            return
        log.i("Start TCP server at %s:%d"%(self.__host,self.__port))
        self.server.serve_forever()
        
