#!/usr/bin/python
# -*- coding: utf-8 -*-

# 异常类
class PibotError(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg
        #Exception.__init__(self,self.__str__())

    def msg(self, msg):
        if not msg is None:return PibotError(self.errcode, msg)
        return PibotError(8,"unknow error")
    def __str__(self):
        return "PibotError:%s(%d)"%(self.errmsg,self.errcode)
    @property
    def message(self):
        return str(self)
# 声明
# 成功
success=PibotError(0,"null")
# 通用失败
fail=PibotError(1,"fail")
# 参数无效
invalidParameter=PibotError(2,"invalid parameter")
# 不支持
noSupport=PibotError(3,"no support")
# 不存在
noExist=PibotError(4,"no exist")
# 超时
timeout=PibotError(5,"timeout")
# 繁忙
busy=PibotError(6,"busy")
# 缺少参数
missParameter=PibotError(7,"miss parameter")
# 系统错误(通用错误)
systemError=PibotError(8,"system error")
# 密码错误
invalidPassword=PibotError(9,"invalid password")
# 编码失败
encodeFailed=PibotError(10,"encode failed")
# 数据库操作失败
dbOpertationFailed=PibotError(11,"db error")
# 已占用
occupied=PibotError(12,"occupied")
# session不存在
noSession = PibotError(13,'cannot find session')
#没有找到
noFound = PibotError(14, "no found")
#已经存在
existed = PibotError(15, "existed")
#已经锁定
locked = PibotError(16, "locked")
#已经过期
expired = PibotError(17, "is expired")
#无效的参数
invalidParameter = PibotError(18, "invalid parameter")

