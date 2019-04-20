#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function

''' 
Transport deals with all the messages from/to a client connection. 
'''
import sys
sys.path.append("..")
import pypibot
from pypibot import log

from Config import *
from Messages import *
from RobotManager import RobotManager
from Utils import bytes_to_int as int
from Utils import int_to_bytes as bytes
import threading
import time


class ParseState:
    WAITING_FOR_BOF = 1
    WAITING_FOR_ID = 2
    WAITING_FOR_LEN = 3
    WAITING_FOR_DATA = 4
    WAITING_FOR_EOF = 5


class Transport(threading.Thread):
    def __init__(self, addr, client):
        threading.Thread.__init__(self)

        self.__shutdown = False
        self.__status = True
        
        log.t('Transport bind to client at %s'%str(addr))
        self.addr = addr
        self.client = client

        # initialize parameters
        self.state = ParseState.WAITING_FOR_BOF
        self.msg_id = None
        self.msg_len = 0
        self.data = b''

    def run(self):
        if ROBOT_STATUS_AUTOFEED:
            auto_feed_thread = threading.Thread(target=self.auto_feed, name='auto_feed'+str(self.addr[1]))
            auto_feed_thread.setDaemon(True)
            auto_feed_thread.start()

        while not self.__shutdown:
            try:
                self.parse(self.client.recv(1))
            except:
                log.w("recv excption")

    def shutdown(self):
        self.__shutdown = True
    
    def check_status(self):
        return self.__status

    def parse(self, c):
        if len(c) == 0: # no data received
            return
        if DEBUG:
            print(self.state)
            print(repr(c))
        if self.state == ParseState.WAITING_FOR_BOF:
            # reset msg 
            self.msg_id = None
            self.msg_len = 0
            self.data = b''

            if c == bytes(BOF):
                if DEBUG:
                    print('got bof')
                self.state += 1
            return
        if self.state == ParseState.WAITING_FOR_ID:
            if DEBUG:
                print('got id ', int(c))
            self.msg_id = int(c)
            self.state += 1
            return
        if self.state == ParseState.WAITING_FOR_LEN:
            if DEBUG:
                print('got len ', int(c))
            self.msg_len = int(c)
            self.state += 1
            return
        if self.state == ParseState.WAITING_FOR_DATA:
            if self.msg_len > 0:
                self.data += c
                self.msg_len -= 1
            else:
                if DEBUG:
                    print('got complete data')
                self.state = ParseState.WAITING_FOR_EOF
        if self.state == ParseState.WAITING_FOR_EOF:
            if c == bytes(EOF):
                if DEBUG:
                    print('got EOF')
                # process message
                self.process_message(self.msg_id, self.data)
            else:
                if DEBUG:
                    print('EOF error, message discarded')
            self.state = ParseState.WAITING_FOR_BOF
            return

    def process_message(self, msg_id, data):
        if DEBUG:
            print("[Transport-", self.addr[1], " processing message id: ", msg_id)
        if msg_id == MsgId.robot_speed_get:
            if DEBUG:
                print('process msg - get speed')
            msg = RobotManager().get_speed()
            self.respond(msg)
            return
        elif msg_id == MsgId.robot_speed_set:
            if DEBUG:
                print('process msg - set speed')
            msg = MsgRobotSpeedSet()
            self.decode(msg, data)
            vx = msg.vx
            vy = msg.vy
            vw = msg.vw
            print(vx, vy, vw)
            RobotManager().set_vel(vx, vy, vw)
            return
        elif msg_id == MsgId.robot_pose_get:
            if DEBUG:
                print('process msg - get pose')
            msg = RobotManager().get_pose()
            self.respond(msg)
            return
        elif msg_id == MsgId.robot_pose_set:
            if DEBUG:
                print('process msg - set pose')
            msg = MsgRobotPoseSet()
            self.decode(msg, data)
            x = msg.x
            y = msg.y
            yaw = msg.yaw
            RobotManager().set_pose(x, y, yaw)
            return

    def respond(self, msg):
        '''send a message back to the paired client'''
        try:
            self.client.sendall(self.encode(msg))
        except:
            self.__status = False
    
    def encode(self, msg):
        ''' encodes a message
            returns a bytes str ready to send
            
            @param msg: a message object
            ---
            @return b_msg: bytes str
        '''
        bof = bytes(BOF)
        eof = bytes(EOF)
        msg_id = bytes(msg.id)
        data = msg.pack()
        msg_len = bytes(len(data)) 
        b_msg = bof + msg_id + msg_len + data + eof
        # if DEBUG:
        #     print(repr(b_msg))
        return b_msg
    
    def decode(self, msg, data):
        ''' decodes a in-coming data into
            a message

            @param msg: a message object
            @param data: received data bytes
            ---
            @return : None
        '''
        msg.unpack(data)   

    def auto_feed(self):
        t_next = time.time()
        t_interval = 1.0/ROBOT_STATUS_AUTOFEED_FREQUENCY
        while True:
            if (time.time() > t_next):
                speed = RobotManager().get_speed()
                msg = MsgRobotSpeedRes()
                msg.vx = speed[0]
                msg.vy = speed[1]
                msg.vw = speed[2]
                self.respond(msg)

                pose = RobotManager().get_pose()
                msg = MsgRobotPoseRes()
                msg.x = pose[0]
                msg.y = pose[1]
                msg.yaw = pose[2]
                self.respond(msg)

                t_next += t_interval            

