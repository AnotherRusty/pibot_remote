#!/usr/bin/env python
#coding=utf-8


'''
    Message classes
'''
import struct
from Config import BOF, EOF, DEBUG
from Utils import int_to_bytes as bytes


class MsgId:    # each message type has a unique id
    # client ----> host
    robot_speed_get = 1
    robot_speed_set = 2
    robot_pose_get = 3
    robot_pose_set = 4

    # host ----> client
    robot_speed_res = 101
    robot_pose_res = 102


#---------------- message definitions--------------------------#
class BasicMessage(object):
    '''Basic message type
        all message types should inherit from this'''
    def pack(self):
        pass
    
    def unpack(self, data):
        pass


class MsgRobotSpeedGet(BasicMessage):
    '''Request for information about the current robot speed'''
    def __init__(self):
        self.id = MsgId.robot_speed_get
    

class MsgRobotSpeedSet(BasicMessage):
    '''Request for setting robot speed'''
    def __init__(self):
        self.id = MsgId.robot_speed_set

        self.vx = 0.0 # float m/s
        self.vy = 0.0 # float m/s
        self.vw = 0.0 # float rad/s
    
    def pack(self):
        data = [self.vx, self.vy, self.vw]
        p = struct.pack('<3f', *data)
        return p
    
    def unpack(self, data):
        [self.vx, self.vy, self.vw] = struct.unpack('<3f', data)


class MsgRobotPoseGet(BasicMessage):
    '''Request for information about the current robot pose'''
    def __init__(self):
        self.id = MsgId.robot_pose_get
    

class MsgRobotPoseSet(BasicMessage):
    '''Request for setting robot pose'''
    def __init__(self):
        self.id = MsgId.robot_pose_set

        self.x = 0.0    # float m
        self.y = 0.0    # float m
        self.yaw = 0.0  # float rad

    def pack(self):
        data = [self.x, self.y, self.yaw]
        p = struct.pack('<3f', *data)
        return p

    def unpack(self, data):
        [self.x, self.y, self.yaw] = struct.unpack('<3f', data)


class MsgRobotSpeedRes(BasicMessage):
    '''Respond with robot speed'''
    def __init__(self):
        self.id = MsgId.robot_speed_res
        # data
        self.vx = 0.0 # float m/s
        self.vy = 0.0 # float m/s
        self.vw = 0.0 # float rad/s
    
    def pack(self):
        data = [self.vx, self.vy, self.vw]
        p = struct.pack('<3f', *data)
        return p
    
    def unpack(self, data):
        [self.vx, self.vy, self.vw] = struct.unpack('<3f', data)


class MsgRobotPoseRes(BasicMessage):
    '''Respond with robot pose'''
    def __init__(self):
        self.id = MsgId.robot_pose_res
        # data
        self.x = 0.0    # float m
        self.y = 0.0    # float m
        self.yaw = 0.0  # float rad

    def pack(self):
        data = [self.x, self.y, self.yaw]
        p = struct.pack('<3f', *data)
        return p
    
    def unpack(self, data):
        [self.x, self.y, self.yaw] = struct.unpack('<3f', data)


    