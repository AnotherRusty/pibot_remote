#!/usr/bin/env python

'''
    Gateway main
'''
from Server import Server
from RobotManager import RobotManager
from Config import HOST, PORT
from sys import exit


assert __name__ == '__main__', 'Please run in main.'

server = Server(HOST, PORT)
server.setDaemon(True)
server.start()

if not RobotManager().init():
    print('Fail to initilize robot manager.')
    exit(1)

RobotManager().spin()

