import os

os.chdir("C:\\Users\\tom_s\\Desktop\\IPASS\\Python")

import pandas as pd
from Algorithm import Algorithm,Neural_network,Linear_regression
from Make_Objects import *
from Test import Test


df1 = pd.read_csv("All_data.csv", index_col=False, encoding="unicode_escape", sep=";")
df2 = pd.read_csv("Fifa_data.csv", index_col=False, encoding="utf-8", sep=";")
match_data = df1 # Save a copy
fifa_data = df2

objects1=Object_initialisation(match_data,fifa_data)
objects1.set_collections()

match_coll,team_coll,player_coll = objects1.match_coll,objects1.team_coll,objects1.player_coll
C1=Calculations()
match_train,match_test=C1.seperateData(match_coll)

L1=Linear_regression(match_coll[:100])
T1=Test(L1,match_coll[:100])
L1.load("L1")
T1.load("T1")

N1=Neural_network(match_coll[:100])
T2=Test(N1,match_coll[:100])
N1.load("N1")
T1.load("T1")





