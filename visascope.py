#coding:utf-8
#复杂示波器程序实例：https://pyvisa.readthedocs.org/en/1.6/example.html

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

#main

rm=visa.ResourceManager()
resource_list=visa.ResourceManager().list_resources()
print resource_list
tkscopeadd=resource_list[0]

tkscope=rm.open_resource(tkscopeadd)
tkscope.write("*rst;status:preset;*cls")

interval_in_ms=500
number_of_readings=10
tkscope.write("status:measurement:enable 512;*sre 1")
tkscope.write("sample:count %d" % number_of_readings)
tkscope.write("trigger:source bus")
tkscope.write("trigger:delay %f"%(interval_in_ms/1000.0))
tkscope.write("trace:points %d" % number_of_readings)
tkscope.write("trace:feed sense1;feed:control next")

tkscope.write("initiate")
tkscope.assert_trigger()
tkscope.wait_for_srq()
