#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function

from Tkinter import *
from Transport import Transport
from Config import HOST, PORT
import threading


def print_speed(speed):
    print(u'[机器人速度] x:', speed[0], ' y:', speed[1], ' w:', speed[2])

def print_pose(pose):
    print(u'[机器人位置] x:', pose[0], ' y:', pose[1], ' yaw:', pose[2])


class MainFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master

        self.createPage()

    def createPage(self):
        Button(self, text='连接', command=self.connect).grid(row=0, sticky=W, pady=10)

        Label(self, text='vx:').grid(row=1, sticky=E)
        Label(self, text='vy:').grid(row=2, sticky=E)
        Label(self, text='vw:').grid(row=3, sticky=E)
        self.entry_vx = Entry(self)
        self.entry_vy = Entry(self)
        self.entry_vw = Entry(self)
        self.entry_vx.grid(row=1, column=1)
        self.entry_vy.grid(row=2, column=1)
        self.entry_vw.grid(row=3, column=1)
        self.entry_vx.insert(0,'0')
        self.entry_vy.insert(0,'0')
        self.entry_vw.insert(0,'0')
        Button(self, text='设置速度', command=self.set_speed).grid(row=4, column=3, sticky=W, pady=10)
        
        Label(self, text='x:').grid(row=5, sticky=E)
        Label(self, text='y:').grid(row=6, sticky=E)
        Label(self, text='yaw:').grid(row=7, sticky=E)
        self.entry_x = Entry(self)
        self.entry_y = Entry(self)
        self.entry_yaw = Entry(self)
        self.entry_x.grid(row=5, column=1)
        self.entry_y.grid(row=6, column=1)
        self.entry_yaw.grid(row=7, column=1)
        self.entry_x.insert(0,'0')
        self.entry_y.insert(0,'0')
        self.entry_yaw.insert(0,'0')
        Button(self, text='设置位置', command=self.set_pose).grid(row=8, column=3, sticky=W, pady=10)
    
    def connect(self):
        # 创建连接
        self.robot = Transport(HOST, PORT)

        # 设置机器人信息反馈回调函数
        self.robot.subscribe_speed(print_speed)
        self.robot.subscribe_pose(print_pose)

        # 启动连接
        self.robot.connect()
        keep = threading.Thread(target=self.keep_connection, name='connection')
        keep.setDaemon(True)
        keep.start()
    
    def keep_connection(self):
        # 保持连接
        self.robot.keep_alive(5)

    def set_speed(self):
        vx = float(self.entry_vx.get())
        vy = float(self.entry_vy.get())
        vw = float(self.entry_vw.get())
        self.robot.set_speed(vx,vy,vw)
    
    def set_pose(self):
        x = float(self.entry_x.get())
        y = float(self.entry_y.get())
        yaw = float(self.entry_yaw.get())
        self.robot.set_pose(x,y,yaw)


if __name__=='__main__':
    root = Tk()
    root.title('pibot remote')
    root.geometry('%dx%d' % (300, 400))
    root.resizable(0,0)
    MainFrame(root).pack()
    root.mainloop()