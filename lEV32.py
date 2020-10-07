'''
Created on Sep 2, 2020
Proof that it is impossible to make a force without a counteforce
Proof that it is impossible to make a force without a counteforce
Proof that it is impossible to make a force without a counteforce
Proof that it is impossible to make a force without a counteforce
Proof that it is impossible to make a force without a counteforce
Proof that it is impossible to make a force without a counteforce
Proof that it is impossible to make a force without a counteforce
@author: wimz
commit ssh 1af81fdf804458fa25f2e8af86b2905aaccfd5ac

verder met laatste. test mislukt

oopn mobile phone this is fighting quotes

wijziging zim zim zim

ja komt binne

'''

import numpy as np

from math import pi
from numpy import arange,sin,cos
import matplotlib.pyplot as plt

import matplotlib.animation as animation
from sympy.physics.units.definitions.dimension_definitions import mass



def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

fig1 = plt.figure()


tstep=0.02  #time step
f=1.0       # frequency
t=0.0       # current time
r=1.0       #radius
mass=1      #mass of object

tstep=0.5  #time step

def nearby(a,b,error):
    if a > b + error*a:
        return False
    if a < b - error*a:
        return False
    return True

assert (    nearby(1,1.01,0.015))
assert (not nearby(1,1.01,0.005))
assert (    nearby(1,0.99,0.015))
assert (not nearby(1,0.99,0.005))

def angle(ti,centerangle,sweepangle, frequency):
    p=[centerangle + sweepangle * sin(t*frequency) for t in ti]
    return p 

def resume(steps,positions):
    # no force applied. same speed. same direction
    for _ in range(steps):
        for j in [0,1]:
            new=positions[j][-1]+positions[j][-1] - positions[j][-2]
            positions[j]+=[new]

def haltit(steps,positions):
    # repeat same positition
    for _ in range(steps):
        for j in [0,1]:
            new=positions[j][-1]
            positions[j]+=[new]

def debug(variable):
    varval=eval(variable)
    print (variable, '=\n', repr(varval) )
    

assert ( nearby( angle([0],1,2,1)[0], 1.0, 0.0001))
assert ( nearby( angle([1],1,2,1)[0],1+2*sin(1*1),0.0001))


centerangle,sweepangle = pi/4.0,pi/8.0

time=arange(-pi/2 , pi/2+tstep, tstep )
ang=angle(time,centerangle,sweepangle, f)

assert ( nearby( np.max(ang), centerangle + sweepangle, 0.01))
assert ( nearby( np.min(ang), centerangle - sweepangle, 0.01))


x = [ 0, 3, 5, 8, 11 ,13] 
y = [ 0, 4, 5, 5, 3, -1] 

# positions =np.array([x,y]) # position at given time
positions = [ x,y]
resume( 3, positions)
haltit( 2, positions)

positions=np.array(positions)

debug ('positions')

# speed depends on previous position and time it took to go there 
Speed = np.diff(positions)/tstep   
debug ('Speed')

# speed depends on previous speed and time it took to change it 
Accel = np.diff(Speed)/tstep
debug ("Accel")


# 
# exit(0)



x = [ r*sin(a) for a in ang] 
y = [ r*cos(a) for a in ang] 

positions =np.array([x,y]) # position at given time


# speed depends on previous position and time it took to go there 
Speed = np.diff(positions)/tstep   
print (Speed)
# speed depends on previous speed and time it took to change it 
Accel = np.diff(Speed)/tstep
print (Accel)




l, = plt.plot([], [], 'r-')

plotdata=positions

plt.xlim(np.amin(plotdata[0]),np.amax(plotdata[0]))
plt.ylim(np.amin(plotdata[1]),np.amax(plotdata[1]))

plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, len(time), fargs=(plotdata, l),
                                    interval=50, blit=True)
# plt.scatter(x,y)
plt.show()



print ("Done" , len(time))
