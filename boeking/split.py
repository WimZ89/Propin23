"""
use pandas to make a list of misc
"""
import pandas as pd

groot_boek = pd.read_csv("58.csv", sep=";")
print(groot_boek.columns)
"""
Index(['Datum', 'Naam / Omschrijving', 'Rekening', 'Tegenrekening', 'Code',
       'Af Bij', 'Bedrag (EUR)', 'Mutatiesoort', 'Mededelingen',
       'Saldo na mutatie', 'Tag'],
"""

tegen_rekeningen = groot_boek['Tegenrekening'].unique()
print(len(tegen_rekeningen))
# print(tegen_rekeningen)

Omschrijving = groot_boek['Naam / Omschrijving'].unique()
print(len(Omschrijving))
# print(Omschrijving)

# for om in Omschrijving:
#     print(om)

cat = open("boekingen.txt", "r").readlines()
print(cat)
lines = [c.split("\t") for c in cat]

print(lines)
new_cat=""
new_cats = []
for l in lines:
    # print(len(l), l[-1])
    if len(l) == 2:
        new_cat = l[-1].strip()
    elif len(l) == 3:
        add_cat = {"category": new_cat, "description": l[-1].strip()} #, "idx":1}
        # print(add_cat)
        new_cats.append(add_cat)

# cats = pd.concat([cats, pd.DataFrame(add_cat)], ignore_index=True)
#
cats = pd.DataFrame(new_cats)
print(cats)
