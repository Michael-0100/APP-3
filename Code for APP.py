import csv

with open ('parcoursup_massive_500000', 'r') as file:
  reader = csv.reader(file, delimiter=';')
  for row in reader:
    print row
import parcoursup_massive_500000
import parcoursup_medium_100000
import parcoursup_programs_massive_5000
import parcoursup_programs_medium_2500
import parcoursup_programs_small_800
import parcoursup_small_10000

