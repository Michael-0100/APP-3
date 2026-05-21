import csv

def load_parcoursup(files):
  datas=[]
  
  for dt in files:
  print(f'data:')
  with open (dt,'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
      data.append(row)
      
    return data

files = [
  'parcoursup_medium_100000.csv',
  'parcoursup_programs_massive_5000.csv',
  'parcoursup_programs_medium_2500.csv',
  'parcoursup_programs_small_800.csv',
  'parcoursup_small_10000.csv',
  'parcoursup_massive_500000.csv'
]

dataset = load_parcoursup(files)

print(3
#testing brand
