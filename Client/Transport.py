#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function


'''
    creates socket connection to the robot
'''

import socket, sys
from time import sleep
import threading
from Utils import bytes_to_int as int
from Utils import int_to_bytes as bytes
from Messages import *
from Config import * 
from RobotStatus import RobotStatus
from threading import Lock


class ParseState:
    WAITING_FOR_BOF = 1
    WAITING_FOR_ID = 2
    WAITING_FOR_LEN = 3
    WAITING_FOR_DATA = 4
    WAITING_FOR_EOF = 5

class Transport():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__robot_status = RobotStatus()
        self.__robot_status_lock = Lock()
        self.__speed_feedback_callback = None
        self.__pose_feedback_callback = None
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__listener = threading.Thread(target=self.__listen, name='listener')
        self.__listener.setDaemon(True)

        self.__parse_state = ParseState.WAITING_FOR_BOF

    ''' API
        启动连接
    '''
    def connect(self):
        self.__socket.connect((self.__host, self.__port))
        print('connected to ', self.__host, ':', self.__port)
        self.__listener.start()

    ''' API
        每次收到机器人速度信息会回调callback
    '''
    def subscribe_speed(self, callback=None):
        self.__speed_feedback_callback = callback

    ''' API
        每次收到机器人位置信息会回调callback
    '''
    def subscribe_pose(self, callback=None):
        self.__pose_feedback_callback = callback

    ''' API
        设置机器人运行速度
    '''
    def set_speed(self, vx, vy, vw):
        msg = MsgRobotPoseSet()
        msg.vx = vx
        msg.vy = vy
        msg.vw = vw
        self.__socket.sendall(self.__encode(msg))
    
    ''' API
        设置机器人位置
    '''
    def set_pose(self, x, y, yaw):
        msg = MsgRobotPoseSet()
        msg.x = x
        msg.y = y
        msg.yaw = y
        self.__socket.sendall(self.__encode(msg))

##################################################
#   private methods
#
    def __parse(self, c):
        if len(c) == 0: # no data received
            return
        if DEBUG:
            print(repr(c))
        if self.__parse_state == ParseState.WAITING_FOR_BOF:
            # reset msg 
            self.msg_id = None
            self.msg_len = 0
            self.data = b''

            if c == bytes(BOF):
                if DEBUG:
                    print('got bof')
                self.__parse_state += 1
            return
        if self.__parse_state == ParseState.WAITING_FOR_ID:
            if DEBUG:
                print('got id ', int(c))
            self.msg_id = int(c)
            self.__parse_state += 1
            return
        if self.__parse_state == ParseState.WAITING_FOR_LEN:
            if DEBUG:
                print('got len ', int(c))
            self.msg_len = int(c)
            self.__parse_state += 1
            return
        if self.__parse_state == ParseState.WAITING_FOR_DATA:
            if self.msg_len > 0:
                self.data += c
                self.msg_len -= 1
            else:
                if DEBUG:
                    print('got complete data')
                self.__parse_state = ParseState.WAITING_FOR_EOF
        if self.__parse_state == ParseState.WAITING_FOR_EOF:
            if c == bytes(EOF):
                if DEBUG:
                    print('got EOF')
                # process message
                self.__process_message(self.msg_id, self.data)
            else:
                if DEBUG:
                    print('EOF error, message discarded')
            self.__parse_state = ParseState.WAITING_FOR_BOF
            return   

    def __listen(self):
        while True:
            incomming_data = self.__socket.recv(1)
            self.__parse(incomming_data)
    
    def __process_message(self, msg_id, data):
        if msg_id == MsgId.robot_speed_res:
            msg = MsgRobotSpeedRes()
            self.__decode(msg, data)
            if self.__robot_status_lock.acquire():
                self.__robot_status.vx = msg.vx
                self.__robot_status.vy = msg.vy
                self.__robot_status.vw = msg.vw
                self.__robot_status_lock.release()
            self.__speed_feedback()
        elif msg_id == MsgId.robot_pose_res:
            msg = MsgRobotPoseRes()
            self.__decode(msg, data)
            if self.__robot_status_lock.acquire():
                self.__robot_status.x = msg.x
                self.__robot_status.y = msg.y
                self.__robot_status.yaw = msg.yaw
                self.__robot_status_lock.release()
            self.__pose_feedback()

    def __encode(self, msg):
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
        if DEBUG:
            print(b_msg)
        return b_msg
    
    def __decode(self, msg, data):
        ''' decodes a in-coming data into
            a message

            @param msg: a message object
            @param data: received data bytes
            ---
            @return : None
        '''
        msg.unpack(data)
    
    def __speed_feedback(self):
        if self.__speed_feedback_callback is None:
            return
        if self.__robot_status_lock.acquire():
            vx = self.__robot_status.vx
            vy = self.__robot_status.vy
            vw = self.__robot_status.vw
            self.__robot_status_lock.release()
        self.__speed_feedback_callback([vx, vy, vw])
    
    def __pose_feedback(self):
        if self.__pose_feedback_callback is None:
            return
        if self.__robot_status_lock.acquire():
            x = self.__robot_status.x
            y = self.__robot_status.y
            yaw = self.__robot_status.yaw
            self.__robot_status_lock.release()
        self.__pose_feedback_callback([x, y, yaw])