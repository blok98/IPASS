import os

os.chdir("C:\\Users\\tom_s\\Desktop\\IPASS\\Python")

import pandas as pd
from Algorithm import Algorithm,Neural_network,Linear_regression
from Make_Objects import *
from Test import Test

import Calculations
from random import sample
from matplotlib import pyplot

df1 = pd.read_csv("All_data.csv", index_col=False, encoding="unicode_escape", sep=";")
df2 = pd.read_csv("Fifa_data.csv", index_col=False, encoding="utf-8", sep=";")
match_data = df1 # Save a copy
fifa_data = df2

#make list of objects Player,Team,Match
objects1=Object_initialisation(match_data,fifa_data)
objects1.set_collections()

match_coll,team_coll,player_coll = objects1.match_coll,objects1.team_coll,objects1.player_coll

L1=Linear_regression(match_coll[:10])
T1=Test(L1,match_coll[:10])
L1.load("L1")
T1.load("T1")
print(L1.model)
print(T1.capital,T1.avg_error)
L1.plot_errors()