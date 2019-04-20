#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os
import datetime
import threading
import assistant
import platform
import thread
import traceback
"""
%a Locale’s abbreviated weekday name.   
%A Locale’s full weekday name.   
%b Locale’s abbreviated month name.   
%B Locale’s full month name.   
%c Locale’s appropriate date and time representation.   
%d Day of the month as a decimal number [01,31].   
%H Hour (24-hour clock) as a decimal number [00,23].   
%I Hour (12-hour clock) as a decimal number [01,12].   
%j Day of the year as a decimal number [001,366].   
%m Month as a decimal number [01,12].   
%M Minute as a decimal number [00,59].   
%p Locale’s equivalent of either AM or PM. (1) 
%S Second as a decimal number [00,61]. (2) 
%U Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0. (3) 
%w Weekday as a decimal number [0(Sunday),6].   
%W Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0. (3) 
%x Locale’s appropriate date representation.   
%X Locale’s appropriate time representation.   
%y Year without century as a decimal number [00,99].   
%Y Year with century as a decimal number.   
%Z Time zone name (no characters if no time zone exists).   
%% A literal '%' character. 

"""
isWindows=False
if platform.system()=='Windows':
    isWindows=True
defaultEncodeing="utf8"
if "-utf8" in sys.argv:
    defaultEncodeing="utf-8"
if "-gbk" in sys.argv:
    defaultEncodeing="gbk"

TRACE=5
DEBUG=4
INFORMATION=3
WARNING=2
ERROR=1
NONE=0

def getLevelFromString(level):
    level=level.lower()
    if level=='t' or level=='trace':return 5
    elif level=='d' or level=='debug':return 4
    elif level=='i' or level=='info':return 3
    elif level=='w' or level=='wran':return 2
    elif level=='e' or level=='error':return 1
    else :return 0
def getLevelString(level):
    if level==TRACE:return "T"
    elif level==DEBUG:return "D"
    elif level==INFORMATION:return "I"
    elif level==WARNING:return "W"
    elif level==ERROR:return "E"
    else:return "N"
class PibotLog:
    def __init__(self):
        self.isEnableControlLog=True
        self.fileTemple=None
        self.filePath=""
        self.level=5
        self._lock=threading.RLock()
        self.fd=None
        self.fd_day=-1
    def setLevel(self,level):
        self.level=getLevelFromString(level)
    def enableControllog(self,enable):
        self.isEnableControlLog=enable
    def enableFileLog(self,fileName):
        self.fileTemple=fileName
        self.updateFilelog()
    def updateFilelog(self):
        fn=assistant.SF(self.fileTemple)
        if fn!=self.filePath:
            self.i("new log file:%s",fn)
            if self.fd:
                self.fd.close()
                self.fd=None
                self.fd_day=-1
                self.filePath=""
            try:
                path=os.path.dirname(fn)
                if path!="" and not os.path.isdir(path):os.makedirs(path)
                self.fd=open(fn,mode="w")
                self.fd_day=datetime.datetime.now().day
                self.filePath=fn
            except Exception as e:
                print("open file fail!file=%s,err=%s"%(fn,e))
    def _output(self,level,msg,args):
        if self.level<level:return
        try:
            if len(args)>0:
                t=[]
                for arg in args:
                    if isinstance(arg,Exception):
                        t.append(traceback.format_exc(arg).decode('utf-8'))
                    elif isinstance(arg,str) :
                        t.append(arg.decode('utf-8'))
                    else:
                        t.append(arg) 
                args=tuple(t)
                try:
                    msg=msg%args
                except:
                    try:
                        for arg in args:
                            msg=msg+str(arg)+" "
                    except Exception as e:
                        msg=msg+"==LOG ERROR==>%s"%(e)
            if len(msg)>4096:msg=msg[0:4096]
            now=datetime.datetime.now()
            msg=msg+"\r\n"
            s="[%s] %04d-%02d-%02d %02d:%02d:%02d.%03d (0x%04X):%s"%(getLevelString(level),now.year,now.month,now.day,now.hour,now.minute,now.second,now.microsecond/1000,(thread.get_ident()>>8)&0xffff,msg)
            prefix=''
            suffix=''
            if not isWindows:
                suffix='\033[0m'
                if level==TRACE:
                    prefix='\033[0;37m'
                elif level==DEBUG:
                    prefix='\033[1m'
                elif level==INFORMATION:
                    prefix='\033[0;32m'          
                elif level==WARNING:
                    prefix='\033[0;33m'          
                elif level==ERROR:
                    prefix='\033[0;31m'          
                else:
                    pass
            self._lock.acquire()
            try:
                if self.isEnableControlLog:
                    sys.stdout.write((prefix+s+suffix).encode(defaultEncodeing))
                if self.fd:
                    if self.fd_day!=now.day:
                        self.updateFilelog()
                    self.fd.write(s.encode('utf-8'))
                    self.fd.flush()
            finally:
                self._lock.release()
        except Exception as e:
            print("PibotLog._output crash!err=%s"%traceback.format_exc(e))
    def trace(self,msg,*args):
        self._output(TRACE,msg,args)
    def t(self,msg,*args):
        self._output(TRACE,msg,args)
    def debug(self,msg,*args):
        self._output(DEBUG, msg,args)
    def d(self,msg,*args):
        self._output(DEBUG, msg,args)
    def info(self,msg,*args):
        self._output(INFORMATION, msg,args)
    def i(self,msg,*args):
        self._output(INFORMATION, msg,args)
    def warn(self,msg,*args):
        self._output(WARNING, msg,args)
    def w(self,msg,*args):
        self._output(WARNING, msg,args)
    def error(self,msg,*args):
        self._output(ERROR, msg,args)
    def e(self,msg,*args):
        self._output(ERROR, msg,args)
    def _log(self,level,msg,args):
        self._output(level, msg,args)
    def createNamedLog(self,name):
        return NamedLog(name)
log=PibotLog()
class NamedLog:
    def __init__(self,name=None):
        global log
        self.name=''
        if name:
            self.name='['+name+']'
        self.log=log
    def trace(self,msg,*args):
        msg=self.name+msg
        self.log._log(TRACE,msg,args)
    def t(self,msg,*args):
        msg=self.name+msg
        self.log._log(TRACE,msg,args)
    def debug(self,msg,*args):
        msg=self.name+msg
        self.log._log(DEBUG, msg,args)
    def d(self,msg,*args):
        msg=self.name+msg
        self.log._log(DEBUG, msg,args)
    def info(self,msg,*args):
        msg=self.name+msg
        self.log._log(INFORMATION, msg,args)
    def i(self,msg,*args):
        msg=self.name+msg
        self.log._log(INFORMATION, msg,args)
    def warn(self,msg,*args):
        msg=self.name+msg
        self.log._log(WARNING, msg,args)
    def w(self,msg,*args):
        msg=self.name+msg
        self.log._log(WARNING, msg,args)
    def error(self,msg,*args):
        msg=self.name+msg
        self.log._log(ERROR, msg,args)
    def e(self,msg,*args):
        msg=self.name+msg
        self.log._log(ERROR, msg,args)
    
if __name__ == "__main__":
    log.trace("1%s","hello")
    log.debug("2%d",12)
    try:
        raise Exception("EXC")
    except Exception as e:
        log.info("3%s",e)
    log.warn("1")
    log.error("1")
    #log.enableFileLog("$(scriptpath)test_$(Date8)_$(filenumber2).log")
    log.trace("1")
    log.debug("1")
    log.info("1")
    log.warn("1")
    log.error("1")
    log=NamedLog("test")
    log.d("1")
    log.i("1")
    log.warn("1")
    log.error("1=%d,%s",100,e)
