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
lines = {c.split("\t") for c in cat}

print(lines)
