#!/usr/bin/env python
#coding=utf-8

''' demo '''


from __future__ import print_function

from Transport import Transport
from Config import HOST, PORT


def print_speed(speed):
    print(u'[机器人速度] x:', speed[0], ' y:', speed[1], ' w:', speed[2])

def print_pose(pose):
    print(u'[机器人位置] x:', pose[0], ' y:', pose[1], ' yaw:', pose[2])


if __name__ == "__main__":
    # 创建连接
    robot = Transport(HOST, PORT)

    # 设置机器人信息反馈回调函数
    robot.subscribe_speed(print_speed)
    robot.subscribe_pose(print_pose)

    # 启动连接
    robot.connect()

    # 保持连接
    robot.keep_alive(5)
