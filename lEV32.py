'''
Created on Sep 2, 2020
Proof that it is impossible to make a force without a counteforce
@author: wimz
'''
from math import pi
from numpy import arange,sin,cos
import matplotlib.pyplot as plt



f=1.0 # frequency
t=0.0 # current time
tstep=0.05 #time step
r=1.0   #radius



def angle(ti):
    p=[pi/4.0 + pi/4.0 * sin(t*f) for t in ti]
    return p 

time=arange(0, 2*pi+tstep, tstep )

# for t in  time:
#     print("%5.2f angle %f"%(t,angle(t)))

ang=angle(time)

# ang=arange(0, pi/4+tstep, tstep )
# ang=arange(0, pi/2+tstep, tstep )

# print (time)
# print (ang)

# plt.plot(time,ang)
# plt.show()

x = [ r*sin(a) for a in ang] 
y = [ r*cos(a) for a in ang] 

plt.plot(x,y)
x=[x+2 for x in x]
plt.plot(x,y)
plt.show()

print ("Done")