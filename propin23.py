'''
Created on May 22, 2021
Force out a box 2nd try
@author: wimz

step 1 dt v s r phi


Fc=m*v*v/r=m*w*w*r
'''

import numpy as np

from math import pi
from numpy import arange,sin,cos

def showvar(variable):
    varval=eval(variable)
    print (variable, '=\n', repr(varval) )

def showarr(variable):
    varval=eval(variable)
    s=variable+ " = "
    for i in varval:
        s+="%5.2f"%i
    print(s) 


tics    = 64
dt      = 0.1  #time each tic
v       = 1 
r       = 1
m       = 1

time = arange(0.0, dt*tics, dt)

showvar ("time")
pos=[0.0]
phi=[0.0]
s = 0.0
a = 0.0
for step in range(tics):
    out=" "
    v+=a*dt
    s +=v*dt
    pos.append(s)
    out+="%6.2f "%s 
    ph = s/r/2/pi*12
    out+="%6.2f "%ph 
    Fc=m*v*v/r
    out+="%6.2f "%Fc 
    print(out)
    
    out+="%6.2f "%Fc 
#     print ("%6.2f %6.2f"%(s,ph))


    
showarr("pos")

