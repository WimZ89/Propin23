'''
Created on Dec 28, 2020
get the hour 
@author: wimz
https://docs.google.com/spreadsheets/d/1W-PMcJUuFpVckV7ScBmmIBxrBChOw_Lk1IHXgyk8szU/edit?usp=sharing

'''

from copy import deepcopy
from datetime import datetime

import pandas as pd
from datetime import datetime

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
new = []
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
    hours = 0.0
    for l in i:
        if l.startswith("DTSTART"):
            t = l.split(":")[1].strip()[:8]
            # print(t)
        if l.startswith("SUMMARY"):
            s = l.split(":")[1].strip()
            first_word = s.split()[0].lower()
            if first_word in ["ziek","werkuren"]:
                hours = s.split(" ")[1]
                hours = hours.replace(",", ".")
                hours = hours.replace("\\", "")

                hours = float(hours)
                try:
                    hours = float(hours)
                except:
                    print("***%s**** in line %s" % (hours, l))
            else:
                pass
                # print ("skip",s,first_word)
    if hours > 0.0:
        work.append("%s : %20s = %f" % (t, s, hours))
        work2.append({"date": t, "hours": hours})

df = pd.DataFrame(work2)

if __name__ == '__main__':
    # hours_worked = 0
    for year in ["2020", "2021", "2022", "2023", "2024", ]:  # uren per jaar
        print(f"________ Overzicht {year}")
        df_work = df[df.date.str[:4] == year]  # filter on year
        duplicates = df_work[df_work.duplicated()]
        if len(duplicates) > 0:
            # seems a google bug. once in editor. twice in log
            print ("ERROR duplicates")
            print(duplicates)
            print ("dropping")
            df_work = df_work.drop_duplicates()
        hours_worked = df_work["hours"].sum()
        print("Totaal uren", year, hours_worked)

# Get today's date
    df_work = df_work.sort_values("date")
    print (df_work.tail(20))
    today = datetime.now()

    # Create a datetime object for January 1st of the current year
    jan_1 = datetime(today.year, 1, 1)

    # Calculate the difference in days between today and January 1st
    days_since_jan_1 = (today - jan_1).days

    print("Days since January 1st this year:", days_since_jan_1)
    expected_hours_worked = frac_year()*1818 # todo verschillend per jaar
    print("Verwachte uren", year, expected_hours_worked)
    print("Gewerkte uren", year, hours_worked)
    print("Teveel gewerkt", hours_worked-expected_hours_worked)

