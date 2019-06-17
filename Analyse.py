import pandas as pd
import numpy as np
import xlrd
import os
import csv



from MyMethods import *

os.chdir('C:\\Users\\tom_s\\Desktop')
df = pd.read_csv ('All_data.csv',header=0,encoding = 'unicode_escape',sep=";")
df2 = pd.read_csv ("Fifa_data.csv",header=0,sep=";")

os.chdir('C:\\Users\\tom_s\\Desktop\\IPASS')
df3 = pd.read_csv ("teamNameMerging.csv",header=0,sep=";")



fifa_clubs=[]
for i in df2["Club"]:
    if i not in fifa_clubs:
        fifa_clubs.append(i)
print("aantal clubs in fifa_clubs",len(fifa_clubs))

wedstrijden_clubs=[]
# for i in df3["res_club"]:
#     if i not in wedstrijden_clubs:
#         wedstrijden_clubs.append(i)
# print("aantal clubs in All_data",len(wedstrijden_clubs))
print(type(df3))

#
# nameMerge=[]
# for i in wedstrijden_clubs:
#     similarClub=""
#     for j in fifa_clubs:
#         try:
#             if i in j or j in i:
#                 nameMerge.append([i,j])
#                 similarClub=j
#         except Exception:
#             pass
#     # print(similarClub)
#
# print(nameMerge)
#
# for key in df:
#     print(key)
#
# hometeams=[]
# divisions=[]
# index=0
# for i in df["HomeTeam"]:
#     if i not in hometeams:
#         hometeams.append(i)
#         divisions.append(df["Div"][index])
#     index+=1
#
# print(len(hometeams))
# print(hometeams)
# print(divisions)
# print(len(divisions))
# for i in hometeams:
#     print(i)
# print("\n\n\n\n")
# for i in divisions:
#     print(i)
# #
# # for i in hometeams:
# #     print(i)