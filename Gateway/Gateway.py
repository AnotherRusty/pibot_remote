#!/usr/bin/env python

'''
    Gateway main
'''
from Server import Server
from RobotManager import RobotManager
from time import sleep
from Config import HOST, PORT
from Utils import input
from sys import exit



assert __name__ == '__main__', 'Please run in main.'

if not RobotManager().init():
    print('Fail to initilize robot manager.')
    exit(1)

server = Server(HOST, PORT)
server.setDaemon(True)
server.start()

sleep(0.5)
while True:
    if input('~:$') == 'q':
        break
exit(0)

