'''
Created on Dec 28, 2020

@author: wimz
'''

from copy import deepcopy

f=open("Uren220.txt", "r")
lines=f.readlines()

items=[]

for i in range(len(lines)):
    l=lines[i]
    if l.startswith("BEGIN:"):
        new=[]
    new.append(l)
    if l.startswith("END:"):
        items.append(deepcopy(new))


work=[]    
for i in items:
    u=0.0
    for l in i:
        if l.startswith("DTSTART"):
            t=l.split(":")[1].strip()
#             print (t)    
        if l.startswith("SUMMARY"):
            s=l.split(":")[1].strip()
            if s.startswith("Werk"):
                u=s.split(" ")[1]
                try:
                    u=float(u)
                except:
                    print ("***%s**** in line %s"%(u,l))
    if u > 0.0:
        work.append("%s : %20s = %f"% (t,s,u))

for w in work:
    print (w)
            