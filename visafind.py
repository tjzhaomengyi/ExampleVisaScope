#coding:utf-8

import visa, sys
#import numpy as np
import matplotlib
import numpy as np
import pylab as pl

_rm=visa.ResourceManager()
if _rm==None:
    print 'The visa resource is empty.'
    sys.exit()

#获得单个仪器信息，参数仪器的硬件接口地址

def getInstrInfo(InstrAdd):
    OpenInstr=_rm.open_resource(InstrAdd)
    InstrInfo=OpenInstr.query('*IDN?')
    return InstrInfo
    

#从示波器中取出一组测量值，默认以list储存,泰克示波器用的是binary方式传输，某些示波器用的是ascII传输
def getCurveVals(InstrAdd):
    #从资源列表中打开仪器
    instr=_rm.open_resource(InstrAdd)
    #从示波器上读取数值
    vals=instr.query_binary_values('CURV?', datatype='d', is_big_endian=True)
    return vals
#    取出一个仪器的仪器会话信息
def getDevSession(InstrAdd):
  device=_rm.open_resource(InstrAdd)
  devsession=device.session
  return devsession
    
    
    
#main
print visa.ResourceManager()
resource_list=_rm.list_resources()
print resource_list

tkscopeadd=resource_list[0]
tkscopeinfo=getInstrInfo(tkscopeadd)
print tkscopeinfo

tkscopevals=getCurveVals(tkscopeadd)
print tkscopevals

tkscopesession=getDevSession(tkscopeadd)
print tkscopesession

#简单从示波器中读取数据，并用matplotlib进行绘图
scopevallen=len(tkscopevals)
print scopevallen
y=tkscopevals
x=range(scopevallen)
pl.plot(x, y)
pl.show()








