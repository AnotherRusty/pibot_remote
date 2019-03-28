#!/usr/bin/env python
#coding=utf-8


''' RobotStatus holds all the information to be monitored about the robot.'''

class RobotStatus():
    def __init__(self):
        ''' velocities '''
        self.vx = float(0)
        self.vy = float(0)
        self.vw = float(0)
        
        ''' pose '''
        self.x = float(0)
        self.y = float(0)
        self.yaw = float(0)

