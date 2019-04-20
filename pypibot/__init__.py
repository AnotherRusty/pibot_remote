#!/usr/bin/python
# -*- coding: utf-8 -*-
from assistant import *
import log as Logger
import err
log=Logger.log
import sys
def createNamedLog(name):
    return Logger.NamedLog(name)
class Object():
    pass
isDebug="-d" in sys.argv

import platform
isWindows=False
if platform.system()=='Windows':
    isWindows=True
