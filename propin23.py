'''
Created on May 22, 2021
Force out a box 2nd try
@author: wimz

step 1 dt v s r phi


Fc=m*v*v/r=m*w*w*r
'''

import numpy as np

from math import pi,sin
from numpy import arange,sin,cos
from twisted.conch.client import direct

def showvar(variable):
    varval=eval(variable)
    print (variable, '=\n', repr(varval) )

def showarr(variable):
    varval=eval(variable)
    s=variable+ " = "
    for i in varval:
        s+="%5.2f"%i
    print(s) 
    
def addvari(s,val):
    s+="%6d ;"%val
    return s

def addvarf(s,val):
#     s+="%6.2f ;"%val
    s+= "{:6.2f}; ".format(val)
    return s

tics    = 64
dt      = 0.1  #time each tic
v       = 1.0 
r       = 1.0
m       = 1.0
F       = 0.0

# time = arange(0.0, dt*tics, dt)
# showvar ("time")
triggers=[j*pi for j in range(10)]
# showvar(triggers)

pos=[0.0]
phi=[0.0]
s = 0.0
a = 0.0
ph = 0.0
step = 0
trigcnt=0;
direction = 1.0
Fsum=0

print ("  step ;  s   ;   tpos;      x;      y;     Fc;    Fcy;      F;      v;   Fsum;")
########     2 ;  0.20;   2.27;   0.93;   0.37;   1.00;   1.00;   1.00;   1.00;   1.00; 
while ph < 24*12.0 :
    step += 1
    out=""
    out = addvari(out,step)
    if ph>triggers[0]:
        direction = -direction
#         print (triggers)
        triggers=triggers[1:]
        trigcnt=2;
    if trigcnt > 0:
        trigcnt -=1
        F=1*direction;
    else:
        F=0
    a=F/m
    v+=a*dt
    s +=v*dt
    pos.append(s)
    out=addvarf(out,s)

    ph = s/r/2/pi*12
#     out=addvarf(out,ph)
    tp=-ph*6/pi+3 # time position
    out=addvarf(out,tp%12.0)
    y,x = sin(ph)*r,cos(ph)*r
    out=addvarf(out,x)
    out=addvarf(out,y)
    Fc  =m*v*v/r
    Fcy =Fc*sin(ph)
    out=addvarf(out,Fc)
    out=addvarf(out,Fcy)
    
    
    out=addvarf(out,F)
    out=addvarf(out,v)

    Fsum += F+Fcy
    out=addvarf(out,Fsum)
    print(out)
    
    out+="%6.2f "%Fc 
#     print ("%6.2f %6.2f"%(s,ph))


    
# showarr("pos")

