'''
Created on Dec 28, 2020
get the hour 
@author: wimz
'''

from copy import deepcopy
import pandas as pd

f = open("old/UREN_hom21kum9j6s2s59jtkk6gijn8@group.calendar.google.com.ics", "r")
lines = f.readlines()

items = []

for i in range(len(lines)):
    l = lines[i]
    if l.startswith("BEGIN:"):
        new = []
    new.append(l)
    if l.startswith("END:"):
        items.append(deepcopy(new))

work = []
work2 = []
for i in items:
    u = 0.0
    for l in i:
        if l.startswith("DTSTART"):
            t = l.split(":")[1].strip()[:8]
            print(t)
        if l.startswith("SUMMARY"):
            s = l.split(":")[1].strip()
            if s.startswith("Werk"):
                u = s.split(" ")[1]
                u = u.replace(",", ".")
                u = u.replace("\\", "")

                u = float(u)
                try:
                    u = float(u)
                except:
                    print("***%s**** in line %s" % (u, l))
    if u > 0.0:
        work.append("%s : %20s = %f" % (t, s, u))
        work2.append({"date": t, "hours": u})

df = pd.DataFrame(work2)

for year in ["2020", "2021", "2022", ]:
    print()
    df21 = df[df.date.str[:4] == year]
    print(year, df21["hours"].sum())
    print(df21["hours"].describe())
    # print(df21["hours"].unique())
# for w in work:
#     print(w)
