'''
Created on Aug 21, 2020

@author: wimz
hoelang niets gedaan?
'''
import sys

print (sys.version)

from pyexcel_ods import get_data

data = get_data("/media/wimz/TDK_8GB/study/kernkwaliteiten.ods")["kernkwaliteiten"]

# import json
# print(json.dumps(data, indent=2, separators=(',', ': ')))

header= data.pop(0)
header = [d.lower() for d in header]
kekwa,vaku,alle,uitd,vw=header
# print (header)
i=1
cnt=1
for kwaliteit in data:
#     kwaliteit = [d.lower() for d in kwaliteit[:4]]
    if (len(kwaliteit)<5):
        break
    for j in range (4):
        kwaliteit[j]=kwaliteit[j].lower()
#     print (kwaliteit)
    voorwerk=kwaliteit[4] > 2
    if voorwerk :
        line  = "%d. Voor de %s %s is de %s %s.\n"%(i,kekwa,kwaliteit[0],vaku,kwaliteit[1]) 
        line += "En de %s is %s, dus de %s is %s\n\n"%(alle,kwaliteit[2],uitd,kwaliteit[3]) 
    #     line += " is de valkuil " +kwaliteit[1] 
        cnt+=1
        print (line)
    i+=1
print (i,cnt)
