#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
from log import PLOG
import os
def getdefaultfilename():
    pass
def openconfiger(filename):
    return configer(filename)
class configer:
    def __init__(self,fullfilepath):
        self._filepath=fullfilepath
        if not os.path.isdir(os.path.dirname(fullfilepath)):
            os.makedirs(os.path.dirname(fullfilepath))
        self._conf=ConfigParser.ConfigParser()
        if os.path.isfile(fullfilepath):
            try:
                self._conf.readfp(open(fullfilepath,"r"))
            except Exception,e:
                PLOG.error("配置文件'%s'打开失败,err=%s"%(self._filepath,e))
    def save(self):
        try:
            self._conf.write(open(self._filepath,"w"))
        except Exception,e:
            PLOG.error("配置文件'%s'保存失败,err=%s"%(self._filepath,e))
            
    def changeConfValue(self,section,option,value):
        if self._conf.has_section(section):
            self._conf.set(section,option,value)
        else:
            self._conf.add_section(section)
            self._conf.set(section,option,value)
            
    def _readvalue(self,fn,section,option,default):
        result=default
        if self._conf.has_section(section):
            if self._conf.has_option(section,option):
                result=fn(section,option)
                PLOG.debug("Option[%s][%s]=%s"%(section,option,str(result)))
            else:
                self._conf.set(section,option,str(default))
                result=default
        else:
            self._conf.add_section(section)
            self._conf.set(section,option,str(default))
            result=default
        return result
    def getstr(self,section,option,default=""):
        return self._readvalue(self._conf.get, section, option, default)
    def getint(self,section,option,default=0):
        return self._readvalue(self._conf.getint, section, option, default)
    def getfloat(self,section,option,default=0.0):
        return self._readvalue(self._conf.getfloat, section, option, default)
    def getboolean(self,section,option,default=False):
        return self._readvalue(self._conf.getboolean, section, option, default)
