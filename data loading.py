import csv

with open ('parcoursup_massive_500000', 'parcoursup_medium_100000','parcoursup_programs_massive_5000','parcoursup_programs_medium_2500', 'parcoursup_programs_small_800','parcoursup_small_10000' ,'r') as file:
  reader = csv.reader(file, delimiter=';')
  for row in reader:
    print (row)
