import pandas as pd
import numpy as np
import xlrd
import os
import csv

from MyMethods import *

os.chdir('C:\\Users\\tom_s\\Desktop')
df = pd.read_csv ('All_data.csv',header=0,encoding = 'unicode_escape')

resultaten = open('All_data.csv','r')
resultaten=csv.DictReader(resultaten)

fifa_data = open("fifa_data.csv",'r',encoding="utf8")
fifa_data = csv.DictReader(fifa_data)


index = 0
fifa_clubs = []
for i in fifa_data:
    if index>9999999999:
        break
    index+=1
    if i["Club"] not in fifa_clubs:
        fifa_clubs.append(i["Club"])

print("\n")

index=0
hometeams=[]
leages=[]
for i in resultaten:
    if index>9999999:
        break
    if [i['HomeTeam'],i['Div']] not in hometeams:
        hometeams.append([i['HomeTeam'],i['Div']])
    if i["Div"] not in leages:
        leages.append(i["Div"])
    index+=1

print("teams wedstrijddata")
printr(hometeams)
print("......aantal teams......")
print(len(hometeams))
printr(leages)
print("\n")
print("\n\n\n")
print("fifa clubs")
printr(fifa_clubs)
print("\n\n\n")

