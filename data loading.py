import csv
files = [
'parcoursup_medium_100000.csv',
'parcoursup_programs_massive_5000.csv',
'parcoursup_programs_medium_2500.csv',
'parcoursup_programs_small_800.csv',
'parcoursup_small_10000.csv',
'parcoursup_massive_500000.csv'
]

for data in files:
  print(f‘data:’)
  with open (data,'r', encoding=“utf-8“) as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
      print (row)


