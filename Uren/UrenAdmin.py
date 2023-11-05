'''
Created on Dec 28, 2020
get the hour 
@author: wimz
https://docs.google.com/spreadsheets/d/1W-PMcJUuFpVckV7ScBmmIBxrBChOw_Lk1IHXgyk8szU/edit?usp=sharing

'''

from copy import deepcopy
from datetime import datetime

import pandas as pd


def frac_year():
    date_obj = datetime.now()

    # Calculate the total number of days in the year
    year = date_obj.year
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365

    # Calculate the day of the year for the given date
    day_of_year = (date_obj - datetime(year, 1, 1)).days + 1

    # Calculate the fraction of the year
    fraction_of_year = day_of_year / days_in_year

    return fraction_of_year


f = open("UREN_hom21kum9j6s2s59jtkk6gijn8@group.calendar.google.com.ics", "r")
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
            # print(t)
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

if __name__ == '__main__':
    for year in ["2020", "2021", "2022", "2023", ]:  # uren per jaar
        print()
        df21 = df[df.date.str[:4] == year]  # filter on year
        # print(df21.to_dict("list"))
        print("Totaal uren", year, df21["hours"].sum())
        print(df21["hours"].describe())
        duplicates = df21[df21.duplicated()]
        if len(duplicates) > 0:
            print(duplicates)
        # print(df21["hours"].unique())
    # for w in work:
    #     print(w)

print("Verwachte uren", year, frac_year()*1818)
