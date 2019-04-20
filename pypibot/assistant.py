#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, inspect
import datetime
import signal
import threading
import time
# function: get directory of current script, if script is built
#   into an executable file, get directory of the excutable file
def current_file_directory():
    path = os.path.realpath(sys.path[0])        # interpreter starter's path
    if os.path.isfile(path):                    # starter is excutable file
        path = os.path.dirname(path)
        path = os.path.abspath(path)            # return excutable file's directory
    else:                                       # starter is python script
        caller_file = inspect.stack()[0][1]     # function caller's filename
        path = os.path.abspath(os.path.dirname(caller_file))# return function caller's file's directory
    if path[-1]!=os.path.sep:path+=os.path.sep
    return path

"""格式化字符串"""
def formatString(string,*argv):
    string=string%argv
    if string.find('$(scriptpath)')>=0:
        string=string.replace('$(scriptpath)',current_file_directory())
    if string.find('$(filenumber2)')>=0:
        i=0
        path=""
        while True:
            path=string.replace('$(scriptpath)',"%02d"%i)
            if not os.path.lexists(path):break
            i+=1
        string=path
    #8位日期（20140404）
    if string.find('$(Date8)')>=0:
        now=datetime.datetime.now()
        string=string.replace('$(Date8)', now.strftime("%Y%m%d"))
    #6位日期（140404）
    if string.find('$(Date6)')>=0:
        now=datetime.datetime.now()
        string=string.replace('$(Date6)', now.strftime("%y%m%d"))
    #6位时间（121212）
    if string.find('$(Time6)')>=0:
        now=datetime.datetime.now()
        string=string.replace('$(Time6)', now.strftime("%H%M%S"))
    #4位时间（1212）
    if string.find('$(Time4)')>=0:
        now=datetime.datetime.now()
        string=string.replace('$(Time4)', now.strftime("%H%M"))
    #文件编号2位（必须在最后）
    if string.find('$(filenumber2)')>=0:
        i=0
        path=""
        while True:
            path=string.replace('$(filenumber2)',"%02d"%i)
            if not os.path.lexists(path):break
            i+=1
        string=path
    #文件编号3位（必须在最后）
    if string.find('$(filenumber3)')>=0:
        i=0
        path=""
        while True:
            path=string.replace('$(filenumber3)',"%03d"%i)
            if not os.path.lexists(path):break
            i+=1
        string=path
    return string

"""
    取得进程列表
    格式：(PID,cmd)
""" 
def getProcessList():
    processList = []
    try:
        for line in os.popen("ps xa"):
            fields = line.split()
            # spid = fields[0]
            pid = 0
            try:pid = int(fields[0])
            except:None
            cmd = line[27:-1]
            # print "PS:%d,%s"%(npid,process)
            if pid != 0 and len(cmd) > 0:
                processList.append((pid, cmd))
    except Exception, e:
        print("getProcessList except:%s" % (e))
    return processList
def killCommand(cmd):
    try:
        processList = getProcessList()
        for p in processList:
            if p[1].find(cmd) != -1:
                pid = p[0]
                os.kill(pid, signal.SIGKILL)
    except Exception, e:
        print("killCommand ‘%s’ except:%s" % (cmd,e))

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    if pid == 0:return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

SF=formatString

#全局异常捕获
def excepthook(excType, excValue, tb):  
    '''''write the unhandle exception to log''' 
    from log import log
    import traceback
    log.e('Unhandled Error: %s',''.join(traceback.format_exception(excType, excValue, tb)))
    sys.exit(-1)
    #sys.__excepthook__(type, value, trace)
    #sys.__excepthook__(excType, excValue, tb)

_defaultGlobalExcept=sys.excepthook

def enableGlobalExcept(enable=True):
    if enable:
        sys.excepthook = excepthook
    else:
        sys.excepthook=_defaultGlobalExcept
# 默认启动全局异常处理
enableGlobalExcept()
#创建线程
def createThread(name,target,args=(),autoRun=True,daemon=True):
    from log import log
    def threadProc():
        log.i("thread %s started!",name)
        try:
            target(*args)
            log.i("thread %s ended!",name)
        except Exception as e:
            log.e("thread %s crash!err=%s",name,e)
    thd=threading.Thread(name=name,target=threadProc)
    thd.setDaemon(daemon)
    if autoRun:thd.start()
    return thd


#定时器
class Timer():
    def __init__(self, timer_proc, args=(),first=0,period=0,name="Timer"):
        self.name=name
        self.first=first
        self.period=period
        self.args=args
        self.timer_proc=timer_proc
        self.thdWork=None
        self.stopFlag=False
        from log import NamedLog
        self.log=NamedLog(name)
    def run(self):
        if self.first>0:
            time.sleep(self.first)
            try:
                self.timer_proc(*self.args)
            except Exception as e:
                self.log.error("timer proc crash!err=%s",e)
        while self.period>0 and not self.stopFlag:
            time.sleep(self.period)
            try:
                self.timer_proc(*self.args)
            except Exception as e:
                self.log.error("timer proc crash!err=%s",e)
    def start(self):
        if self.isAlive():
            self.log.d("already running!")
            return True
        self.stopFlag=False
        self.thdWork=threading.Thread(name=self.name,target=self.run)
        self.thdWork.setDaemon(True)
        self.thdWork.start()
    def stop(self,timeout=3):
        if self.isAlive():
            self.stopFlag=True
            try:
                self.thdWork.join(timeout)
            except Exception as e:
                self.log.e("stop timeout!")

    def isAlive(self):
        return self.thdWork and self.thdWork.isAlive()
#计时器
class Ticker():
    def __init__(self):
        self.reset()
        # 片段,可以判断时长是否在一个特定毫秒段内
        self.section=[]
    def reset(self):
        self.tick=time.time()
        self.end=0
    def stop(self):
        self.end=time.time()
    @property
    def ticker(self):
        if self.end==0:
            return int((time.time()-self.tick)*1000)
        else:
            return int((self.end-self.tick)*1000)
    def addSection(self,a,b):
        a,b=int(a),int(b)
        assert a<b
        self.section.append((a,b))
    def removeSection(self,a,b):
        a,b=int(a),int(b)
        self.section.remove((a,b))
    def removeAllSectioin(self):
        self.section=[]
    def inSection(self):
        tick=self.ticker
        for (a,b) in self.section:
            if tick>=a and tick<=b:
                return True
        return False
    def __call__(self):
        return self.ticker
def waitExit():
    import log
    log.log.i("start waiting to exit...")
    try:
        while(True):
            time.sleep(1)
    except Exception as e:
        log.log.w("recv exit sign!")
    