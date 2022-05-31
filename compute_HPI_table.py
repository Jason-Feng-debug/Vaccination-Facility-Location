#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 11, 2022
@Author: Jingyuan Hu
"""

import os
import pandas as pd
import numpy as np
from tabulate import tabulate

os.chdir('/Users/jingyuanhu/Desktop/Research/COVID_project/Submission MS/Code')

###########################################################################

### Census Tract ###
CA_TRACT = pd.read_csv('../Result/Tract_0.84capacity_N10/CA_Tract_N10.csv', delimiter = ",")
Quartile = CA_TRACT['HPIQuartile'].values
Population = CA_TRACT['Population'].values
total_population = sum(Population)

population1 = sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Population'].values)
population2 = sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Population'].values)
population3 = sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Population'].values)
population4 = sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Population'].values)
population_vec = [total_population, population1, population2, population3, population4]

C_current = np.genfromtxt('../Data/dist_matrix_CA_current_tract.csv', delimiter = ",", dtype = float)
C_current = C_current.astype(int)
C_current = C_current.T
num_zips, num_current_stores = np.shape(C_current)
   
C_dollar = np.genfromtxt('../Data/dist_matrix_CA_dollar_tract.csv', delimiter = ",", dtype = float)
C_dollar = C_dollar.astype(int)
C_dollar = C_dollar.T
num_zips, num_dollar_stores = np.shape(C_dollar)

C_total = np.concatenate((C_current, C_dollar), axis = 1)
num_total_stores = num_current_stores + num_dollar_stores

###########################################################################

### Demand ###
F_D_total = 0.755 - 0.069 * np.log(C_total/1000)
F_D_current = F_D_total[:,0:num_current_stores]

F_DH_total = []
for i in range(num_zips):
    
    zip_quartile = Quartile[i]
    
    if zip_quartile == 1:
        zip_willingness = (0.826 - 0.146) - (0.016 + 0.053) * np.log(C_total[i,:]/1000)  
    elif zip_quartile == 2:
        zip_willingness = (0.826 - 0.097) - (0.016 + 0.047) * np.log(C_total[i,:]/1000)
    elif zip_quartile == 3:
        zip_willingness = (0.826 - 0.077) - (0.016 + 0.039) * np.log(C_total[i,:]/1000)
    elif zip_quartile == 4:
        zip_willingness = 0.826 - 0.016 * np.log(C_total[i,:]/1000)
    else:
        # two zip code with NA quantile, use the general equation
        zip_willingness = 0.755 - 0.069 * np.log(C_total[i,:]/1000)
    
    F_DH_total.append(zip_willingness)
    
F_DH_total = np.asarray(F_DH_total)
F_DH_current = F_DH_total[:,0:num_current_stores]

###########################################################################

### Solution ###
path = '../Result/Tract_0.84capacity_N10/'

y_current = np.genfromtxt(path + 'Dist/y_current.csv', delimiter = ",", dtype = float)
y_current_hpi = np.genfromtxt(path + 'HPI_Dist/y_current.csv', delimiter = ",", dtype = float)
y_total = np.genfromtxt(path + 'Dist/y_total.csv', delimiter = ",", dtype = float)
y_total_hpi = np.genfromtxt(path + 'HPI_Dist/y_total.csv', delimiter = ",", dtype = float)

mat_y_current = np.reshape(y_current, (num_zips, num_current_stores))
mat_y_current_hpi = np.reshape(y_current_hpi, (num_zips, num_current_stores))
mat_y_total = np.reshape(y_total, (num_zips, num_total_stores))
mat_y_total_hpi = np.reshape(y_total_hpi, (num_zips, num_total_stores))

CURRENT = pd.read_csv(path + 'CurrentStores_Tract_N10.csv', delimiter = ",")
DOLLAR = pd.read_csv(path + 'DollarStores_Tract_N10.csv', delimiter = ",")


###########################################################################

###########################################################################

### Proportion of demand covered by each store ###

### Current + Dist
CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
Tract1Pharmacy1 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy1_Current_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy2 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy2_Current_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy3 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy3_Current_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy4 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy4_Current_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1

CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
Tract2Pharmacy1 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy1_Current_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy2 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy2_Current_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy3 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy3_Current_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy4 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy4_Current_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2

CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
Tract3Pharmacy1 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy1_Current_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy2 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy2_Current_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy3 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy3_Current_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy4 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy4_Current_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3

CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]
Tract4Pharmacy1 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy1_Current_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy2 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy2_Current_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy3 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy3_Current_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy4 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy4_Current_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4

table = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4],
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4],
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4],
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4]]) * 100, 2)
print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

sum_one = Tract1Pharmacy1 + Tract1Pharmacy2 + Tract1Pharmacy3 + Tract1Pharmacy4
sum_two = Tract2Pharmacy1 + Tract2Pharmacy2 + Tract2Pharmacy3 + Tract2Pharmacy4
sum_three = Tract3Pharmacy1 + Tract3Pharmacy2 + Tract3Pharmacy3 + Tract3Pharmacy4
sum_four = Tract4Pharmacy1 + Tract4Pharmacy2 + Tract4Pharmacy3 + Tract4Pharmacy4

table_scaled = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4]/sum_one,
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4]/sum_two,
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4]/sum_three,
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4]/sum_four]) * 100, 2)
print(tabulate(table_scaled, tablefmt="latex", floatfmt=".1f"))


### Current + DistHPI
CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
Tract1Pharmacy1 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy1_Current_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy2 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy2_Current_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy3 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy3_Current_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy4 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy4_Current_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1

CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
Tract2Pharmacy1 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy1_Current_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy2 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy2_Current_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy3 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy3_Current_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy4 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy4_Current_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2

CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
Tract3Pharmacy1 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy1_Current_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy2 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy2_Current_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy3 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy3_Current_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy4 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy4_Current_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3

CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]
Tract4Pharmacy1 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy1_Current_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy2 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy2_Current_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy3 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy3_Current_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy4 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy4_Current_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4

table = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4],
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4],
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4],
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4]]) * 100, 2)
print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

sum_one = Tract1Pharmacy1 + Tract1Pharmacy2 + Tract1Pharmacy3 + Tract1Pharmacy4
sum_two = Tract2Pharmacy1 + Tract2Pharmacy2 + Tract2Pharmacy3 + Tract2Pharmacy4
sum_three = Tract3Pharmacy1 + Tract3Pharmacy2 + Tract3Pharmacy3 + Tract3Pharmacy4
sum_four = Tract4Pharmacy1 + Tract4Pharmacy2 + Tract4Pharmacy3 + Tract4Pharmacy4

table_scaled = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4]/sum_one,
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4]/sum_two,
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4]/sum_three,
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4]/sum_four]) * 100, 2)
print(tabulate(table_scaled, tablefmt="latex", floatfmt=".1f"))


### Both + Dist
CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
Tract1Pharmacy1 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy1_Total_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy2 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy2_Total_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy3 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy3_Total_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy4 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy4_Total_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Dollar1 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar1_Total_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Dollar2 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar2_Total_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Dollar3 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar3_Total_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Dollar4 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar4_Total_Dist'] * CA_TRACT_QUARTILE1['Population']) / population1

CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
Tract2Pharmacy1 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy1_Total_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy2 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy2_Total_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy3 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy3_Total_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy4 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy4_Total_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Dollar1 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar1_Total_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Dollar2 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar2_Total_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Dollar3 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar3_Total_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Dollar4 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar4_Total_Dist'] * CA_TRACT_QUARTILE2['Population']) / population2

CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
Tract3Pharmacy1 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy1_Total_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy2 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy2_Total_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy3 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy3_Total_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy4 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy4_Total_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Dollar1 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar1_Total_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Dollar2 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar2_Total_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Dollar3 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar3_Total_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Dollar4 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar4_Total_Dist'] * CA_TRACT_QUARTILE3['Population']) / population3

CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]
Tract4Pharmacy1 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy1_Total_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy2 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy2_Total_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy3 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy3_Total_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy4 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy4_Total_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Dollar1 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar1_Total_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Dollar2 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar2_Total_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Dollar3 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar3_Total_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Dollar4 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar4_Total_Dist'] * CA_TRACT_QUARTILE4['Population']) / population4

np.set_printoptions(suppress=True) # don't use scientific notation
table = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4, 
                            Tract1Dollar1, Tract1Dollar2, Tract1Dollar3, Tract1Dollar4],
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4,
                            Tract2Dollar1, Tract2Dollar2, Tract2Dollar3, Tract2Dollar4],
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4,
                            Tract3Dollar1, Tract3Dollar2, Tract3Dollar3, Tract3Dollar4],
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4,
                            Tract4Dollar1, Tract4Dollar2, Tract4Dollar3, Tract4Dollar4]]) * 100, 2)
print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

sum_one = Tract1Pharmacy1 + Tract1Pharmacy2 + Tract1Pharmacy3 + Tract1Pharmacy4 + Tract1Dollar1 + Tract1Dollar2 + Tract1Dollar3 + Tract1Dollar4
sum_two = Tract2Pharmacy1 + Tract2Pharmacy2 + Tract2Pharmacy3 + Tract2Pharmacy4 + Tract2Dollar1 + Tract2Dollar2 + Tract2Dollar3 + Tract2Dollar4
sum_three = Tract3Pharmacy1 + Tract3Pharmacy2 + Tract3Pharmacy3 + Tract3Pharmacy4 + Tract3Dollar1 + Tract3Dollar2 + Tract3Dollar3 + Tract3Dollar4
sum_four = Tract4Pharmacy1 + Tract4Pharmacy2 + Tract4Pharmacy3 + Tract4Pharmacy4 + Tract4Dollar1 + Tract4Dollar2 + Tract4Dollar3 + Tract4Dollar4

table_scaled = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4, 
                                   Tract1Dollar1, Tract1Dollar2, Tract1Dollar3, Tract1Dollar4] / sum_one,
                                  [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4,
                                   Tract2Dollar1, Tract2Dollar2, Tract2Dollar3, Tract2Dollar4] / sum_two,
                                  [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4,
                                   Tract3Dollar1, Tract3Dollar2, Tract3Dollar3, Tract3Dollar4] / sum_three,
                                  [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4,
                                   Tract4Dollar1, Tract4Dollar2, Tract4Dollar3, Tract4Dollar4] / sum_four]) * 100, 2)

print(tabulate(table_scaled, tablefmt="latex", floatfmt=".1f"))


### Both + DistHPI
CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
Tract1Pharmacy1 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy1_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy2 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy2_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy3 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy3_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Pharmacy4 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy4_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Dollar1 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar1_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Dollar2 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar2_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Dollar3 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar3_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1
Tract1Dollar4 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar4_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population']) / population1

CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
Tract2Pharmacy1 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy1_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy2 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy2_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy3 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy3_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Pharmacy4 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy4_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Dollar1 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar1_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Dollar2 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar2_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Dollar3 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar3_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2
Tract2Dollar4 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar4_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population']) / population2

CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
Tract3Pharmacy1 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy1_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy2 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy2_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy3 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy3_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Pharmacy4 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy4_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Dollar1 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar1_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Dollar2 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar2_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Dollar3 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar3_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3
Tract3Dollar4 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar4_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population']) / population3

CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]
Tract4Pharmacy1 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy1_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy2 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy2_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy3 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy3_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Pharmacy4 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy4_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Dollar1 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar1_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Dollar2 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar2_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Dollar3 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar3_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4
Tract4Dollar4 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar4_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population']) / population4

np.set_printoptions(suppress=True) # don't use scientific notation
table = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4, 
                            Tract1Dollar1, Tract1Dollar2, Tract1Dollar3, Tract1Dollar4],
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4,
                            Tract2Dollar1, Tract2Dollar2, Tract2Dollar3, Tract2Dollar4],
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4,
                            Tract3Dollar1, Tract3Dollar2, Tract3Dollar3, Tract3Dollar4],
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4,
                            Tract4Dollar1, Tract4Dollar2, Tract4Dollar3, Tract4Dollar4]]) * 100, 2)
print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

sum_one = Tract1Pharmacy1 + Tract1Pharmacy2 + Tract1Pharmacy3 + Tract1Pharmacy4 + Tract1Dollar1 + Tract1Dollar2 + Tract1Dollar3 + Tract1Dollar4
sum_two = Tract2Pharmacy1 + Tract2Pharmacy2 + Tract2Pharmacy3 + Tract2Pharmacy4 + Tract2Dollar1 + Tract2Dollar2 + Tract2Dollar3 + Tract2Dollar4
sum_three = Tract3Pharmacy1 + Tract3Pharmacy2 + Tract3Pharmacy3 + Tract3Pharmacy4 + Tract3Dollar1 + Tract3Dollar2 + Tract3Dollar3 + Tract3Dollar4
sum_four = Tract4Pharmacy1 + Tract4Pharmacy2 + Tract4Pharmacy3 + Tract4Pharmacy4 + Tract4Dollar1 + Tract4Dollar2 + Tract4Dollar3 + Tract4Dollar4

table_scaled = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4, 
                                   Tract1Dollar1, Tract1Dollar2, Tract1Dollar3, Tract1Dollar4] / sum_one,
                                  [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4,
                                   Tract2Dollar1, Tract2Dollar2, Tract2Dollar3, Tract2Dollar4] / sum_two,
                                  [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4,
                                   Tract3Dollar1, Tract3Dollar2, Tract3Dollar3, Tract3Dollar4] / sum_three,
                                  [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4,
                                   Tract4Dollar1, Tract4Dollar2, Tract4Dollar3, Tract4Dollar4] / sum_four]) * 100, 2)

print(tabulate(table_scaled, tablefmt="latex", floatfmt=".1f"))


###########################################################################

###########################################################################

### Population covered by each store ###

### Current + Dist
CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
Tract1Pharmacy1 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy1_Current_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy2 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy2_Current_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy3 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy3_Current_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy4 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy4_Current_Dist'] * CA_TRACT_QUARTILE1['Population'])

CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
Tract2Pharmacy1 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy1_Current_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy2 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy2_Current_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy3 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy3_Current_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy4 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy4_Current_Dist'] * CA_TRACT_QUARTILE2['Population'])

CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
Tract3Pharmacy1 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy1_Current_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy2 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy2_Current_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy3 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy3_Current_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy4 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy4_Current_Dist'] * CA_TRACT_QUARTILE3['Population'])

CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]
Tract4Pharmacy1 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy1_Current_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy2 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy2_Current_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy3 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy3_Current_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy4 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy4_Current_Dist'] * CA_TRACT_QUARTILE4['Population'])

table = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4],
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4],
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4],
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4]])/ 1000000, 2)
print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

### Current + DistHPI
CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
Tract1Pharmacy1 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy1_Current_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy2 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy2_Current_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy3 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy3_Current_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy4 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy4_Current_DistHPI'] * CA_TRACT_QUARTILE1['Population'])

CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
Tract2Pharmacy1 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy1_Current_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy2 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy2_Current_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy3 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy3_Current_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy4 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy4_Current_DistHPI'] * CA_TRACT_QUARTILE2['Population'])

CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
Tract3Pharmacy1 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy1_Current_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy2 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy2_Current_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy3 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy3_Current_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy4 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy4_Current_DistHPI'] * CA_TRACT_QUARTILE3['Population'])

CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]
Tract4Pharmacy1 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy1_Current_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy2 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy2_Current_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy3 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy3_Current_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy4 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy4_Current_DistHPI'] * CA_TRACT_QUARTILE4['Population'])

table = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4],
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4],
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4],
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4]]) / 1000000, 2)
print(tabulate(table, tablefmt="latex", floatfmt=".2f"))


### Both + Dist
CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
Tract1Pharmacy1 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy1_Total_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy2 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy2_Total_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy3 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy3_Total_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy4 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy4_Total_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Dollar1 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar1_Total_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Dollar2 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar2_Total_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Dollar3 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar3_Total_Dist'] * CA_TRACT_QUARTILE1['Population'])
Tract1Dollar4 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar4_Total_Dist'] * CA_TRACT_QUARTILE1['Population'])

CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
Tract2Pharmacy1 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy1_Total_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy2 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy2_Total_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy3 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy3_Total_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy4 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy4_Total_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Dollar1 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar1_Total_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Dollar2 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar2_Total_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Dollar3 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar3_Total_Dist'] * CA_TRACT_QUARTILE2['Population'])
Tract2Dollar4 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar4_Total_Dist'] * CA_TRACT_QUARTILE2['Population'])

CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
Tract3Pharmacy1 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy1_Total_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy2 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy2_Total_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy3 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy3_Total_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy4 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy4_Total_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Dollar1 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar1_Total_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Dollar2 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar2_Total_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Dollar3 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar3_Total_Dist'] * CA_TRACT_QUARTILE3['Population'])
Tract3Dollar4 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar4_Total_Dist'] * CA_TRACT_QUARTILE3['Population'])

CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]
Tract4Pharmacy1 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy1_Total_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy2 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy2_Total_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy3 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy3_Total_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy4 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy4_Total_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Dollar1 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar1_Total_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Dollar2 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar2_Total_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Dollar3 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar3_Total_Dist'] * CA_TRACT_QUARTILE4['Population'])
Tract4Dollar4 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar4_Total_Dist'] * CA_TRACT_QUARTILE4['Population'])

np.set_printoptions(suppress=True) # don't use scientific notation
table = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4, 
                            Tract1Dollar1, Tract1Dollar2, Tract1Dollar3, Tract1Dollar4],
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4,
                            Tract2Dollar1, Tract2Dollar2, Tract2Dollar3, Tract2Dollar4],
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4,
                            Tract3Dollar1, Tract3Dollar2, Tract3Dollar3, Tract3Dollar4],
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4,
                            Tract4Dollar1, Tract4Dollar2, Tract4Dollar3, Tract4Dollar4]]) / 1000000, 2)
print(tabulate(table, tablefmt="latex", floatfmt=".2f"))


### Both + DistHPI
CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
Tract1Pharmacy1 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy1_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy2 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy2_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy3 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy3_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Pharmacy4 = sum(CA_TRACT_QUARTILE1['Demand_by_Pharmacy4_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Dollar1 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar1_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Dollar2 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar2_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Dollar3 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar3_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population'])
Tract1Dollar4 = sum(CA_TRACT_QUARTILE1['Demand_by_Dollar4_Total_DistHPI'] * CA_TRACT_QUARTILE1['Population'])

CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
Tract2Pharmacy1 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy1_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy2 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy2_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy3 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy3_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Pharmacy4 = sum(CA_TRACT_QUARTILE2['Demand_by_Pharmacy4_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Dollar1 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar1_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Dollar2 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar2_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Dollar3 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar3_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population'])
Tract2Dollar4 = sum(CA_TRACT_QUARTILE2['Demand_by_Dollar4_Total_DistHPI'] * CA_TRACT_QUARTILE2['Population'])

CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
Tract3Pharmacy1 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy1_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy2 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy2_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy3 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy3_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Pharmacy4 = sum(CA_TRACT_QUARTILE3['Demand_by_Pharmacy4_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Dollar1 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar1_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Dollar2 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar2_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Dollar3 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar3_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population'])
Tract3Dollar4 = sum(CA_TRACT_QUARTILE3['Demand_by_Dollar4_Total_DistHPI'] * CA_TRACT_QUARTILE3['Population'])

CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]
Tract4Pharmacy1 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy1_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy2 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy2_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy3 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy3_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Pharmacy4 = sum(CA_TRACT_QUARTILE4['Demand_by_Pharmacy4_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Dollar1 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar1_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Dollar2 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar2_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Dollar3 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar3_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population'])
Tract4Dollar4 = sum(CA_TRACT_QUARTILE4['Demand_by_Dollar4_Total_DistHPI'] * CA_TRACT_QUARTILE4['Population'])

np.set_printoptions(suppress=True) # don't use scientific notation
table = np.round(np.array([[Tract1Pharmacy1, Tract1Pharmacy2, Tract1Pharmacy3, Tract1Pharmacy4, 
                            Tract1Dollar1, Tract1Dollar2, Tract1Dollar3, Tract1Dollar4],
                           [Tract2Pharmacy1, Tract2Pharmacy2, Tract2Pharmacy3, Tract2Pharmacy4,
                            Tract2Dollar1, Tract2Dollar2, Tract2Dollar3, Tract2Dollar4],
                           [Tract3Pharmacy1, Tract3Pharmacy2, Tract3Pharmacy3, Tract3Pharmacy4,
                            Tract3Dollar1, Tract3Dollar2, Tract3Dollar3, Tract3Dollar4],
                           [Tract4Pharmacy1, Tract4Pharmacy2, Tract4Pharmacy3, Tract4Pharmacy4,
                            Tract4Dollar1, Tract4Dollar2, Tract4Dollar3, Tract4Dollar4]]) / 1000000, 2)
print(tabulate(table, tablefmt="latex", floatfmt=".2f"))


###########################################################################

###########################################################################

### Proportion of capacity allocated to each tract ###

### Current + Dist
CURRENT_QUARTILE1 = CURRENT[CURRENT['HPIQuartile'] == 1]
CURRENT_QUARTILE2 = CURRENT[CURRENT['HPIQuartile'] == 2]
CURRENT_QUARTILE3 = CURRENT[CURRENT['HPIQuartile'] == 3]
CURRENT_QUARTILE4 = CURRENT[CURRENT['HPIQuartile'] == 4]

table = np.round(np.array([[np.mean(CURRENT_QUARTILE1['Utilization_HPI1_Current_Dist']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI2_Current_Dist']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI3_Current_Dist']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI4_Current_Dist'])],
                           [np.mean(CURRENT_QUARTILE2['Utilization_HPI1_Current_Dist']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI2_Current_Dist']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI3_Current_Dist']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI4_Current_Dist'])],
                           [np.mean(CURRENT_QUARTILE3['Utilization_HPI1_Current_Dist']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI2_Current_Dist']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI3_Current_Dist']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI4_Current_Dist'])],
                           [np.mean(CURRENT_QUARTILE4['Utilization_HPI1_Current_Dist']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI2_Current_Dist']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI3_Current_Dist']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI4_Current_Dist'])]
                           ]) * 100, 2)

print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

table_var = np.round(np.array([[np.var(CURRENT_QUARTILE1['Utilization_HPI1_Current_Dist']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI2_Current_Dist']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI3_Current_Dist']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI4_Current_Dist'])],
                           [np.var(CURRENT_QUARTILE2['Utilization_HPI1_Current_Dist']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI2_Current_Dist']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI3_Current_Dist']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI4_Current_Dist'])],
                           [np.var(CURRENT_QUARTILE3['Utilization_HPI1_Current_Dist']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI2_Current_Dist']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI3_Current_Dist']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI4_Current_Dist'])],
                           [np.var(CURRENT_QUARTILE4['Utilization_HPI1_Current_Dist']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI2_Current_Dist']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI3_Current_Dist']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI4_Current_Dist'])]
                           ]) * 100, 1)

print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))

total1 = CURRENT_QUARTILE1['Utilization_HPI1_Current_Dist'] +\
    CURRENT_QUARTILE1['Utilization_HPI2_Current_Dist'] +\
        CURRENT_QUARTILE1['Utilization_HPI3_Current_Dist']+\
            CURRENT_QUARTILE1['Utilization_HPI4_Current_Dist']
    
total2 = CURRENT_QUARTILE2['Utilization_HPI1_Current_Dist'] +\
    CURRENT_QUARTILE2['Utilization_HPI2_Current_Dist'] +\
        CURRENT_QUARTILE2['Utilization_HPI3_Current_Dist']+\
            CURRENT_QUARTILE2['Utilization_HPI4_Current_Dist']
            
total3 = CURRENT_QUARTILE3['Utilization_HPI1_Current_Dist'] +\
    CURRENT_QUARTILE3['Utilization_HPI2_Current_Dist'] +\
        CURRENT_QUARTILE3['Utilization_HPI3_Current_Dist']+\
            CURRENT_QUARTILE3['Utilization_HPI4_Current_Dist']            
            
total4 = CURRENT_QUARTILE4['Utilization_HPI1_Current_Dist'] +\
    CURRENT_QUARTILE4['Utilization_HPI2_Current_Dist'] +\
        CURRENT_QUARTILE4['Utilization_HPI3_Current_Dist']+\
            CURRENT_QUARTILE4['Utilization_HPI4_Current_Dist']
            
table_total = np.round(np.array([[np.mean(total1), np.var(total1)],
                                 [np.mean(total2), np.var(total2)],
                                 [np.mean(total3), np.var(total3)],
                                 [np.mean(total4), np.var(total4)]
                                 ]) * 100, 1)

print(tabulate(table_total, tablefmt="latex", floatfmt=".1f"))


### Current + DistHPI
table = np.round(np.array([[np.mean(CURRENT_QUARTILE1['Utilization_HPI1_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI2_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI3_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI4_Current_DistHPI'])],
                           [np.mean(CURRENT_QUARTILE2['Utilization_HPI1_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI2_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI3_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI4_Current_DistHPI'])],
                           [np.mean(CURRENT_QUARTILE3['Utilization_HPI1_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI2_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI3_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI4_Current_DistHPI'])],
                           [np.mean(CURRENT_QUARTILE4['Utilization_HPI1_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI2_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI3_Current_DistHPI']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI4_Current_DistHPI'])]
                           ]) * 100, 2)

print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

table_var = np.round(np.array([[np.var(CURRENT_QUARTILE1['Utilization_HPI1_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI2_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI3_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI4_Current_DistHPI'])],
                           [np.var(CURRENT_QUARTILE2['Utilization_HPI1_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI2_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI3_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI4_Current_DistHPI'])],
                           [np.var(CURRENT_QUARTILE3['Utilization_HPI1_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI2_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI3_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI4_Current_DistHPI'])],
                           [np.var(CURRENT_QUARTILE4['Utilization_HPI1_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI2_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI3_Current_DistHPI']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI4_Current_DistHPI'])]
                           ]) * 100, 1)

print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))

total1 = CURRENT_QUARTILE1['Utilization_HPI1_Current_DistHPI'] +\
    CURRENT_QUARTILE1['Utilization_HPI2_Current_DistHPI'] +\
        CURRENT_QUARTILE1['Utilization_HPI3_Current_DistHPI']+\
            CURRENT_QUARTILE1['Utilization_HPI4_Current_DistHPI']
    
total2 = CURRENT_QUARTILE2['Utilization_HPI1_Current_DistHPI'] +\
    CURRENT_QUARTILE2['Utilization_HPI2_Current_DistHPI'] +\
        CURRENT_QUARTILE2['Utilization_HPI3_Current_DistHPI']+\
            CURRENT_QUARTILE2['Utilization_HPI4_Current_DistHPI']
            
total3 = CURRENT_QUARTILE3['Utilization_HPI1_Current_DistHPI'] +\
    CURRENT_QUARTILE3['Utilization_HPI2_Current_DistHPI'] +\
        CURRENT_QUARTILE3['Utilization_HPI3_Current_DistHPI']+\
            CURRENT_QUARTILE3['Utilization_HPI4_Current_DistHPI']            
            
total4 = CURRENT_QUARTILE4['Utilization_HPI1_Current_DistHPI'] +\
    CURRENT_QUARTILE4['Utilization_HPI2_Current_DistHPI'] +\
        CURRENT_QUARTILE4['Utilization_HPI3_Current_DistHPI']+\
            CURRENT_QUARTILE4['Utilization_HPI4_Current_DistHPI']
            
table_total = np.round(np.array([[np.mean(total1), np.var(total1)],
                                 [np.mean(total2), np.var(total2)],
                                 [np.mean(total3), np.var(total3)],
                                 [np.mean(total4), np.var(total4)]
                                 ]) * 100, 1)

print(tabulate(table_total, tablefmt="latex", floatfmt=".1f"))


### Total + Dist
CURRENT_QUARTILE1 = CURRENT[(CURRENT['HPIQuartile'] == 1) & (CURRENT['Selected_Total_Dist'] == 1)]
CURRENT_QUARTILE2 = CURRENT[(CURRENT['HPIQuartile'] == 2) & (CURRENT['Selected_Total_Dist'] == 1)]
CURRENT_QUARTILE3 = CURRENT[(CURRENT['HPIQuartile'] == 3) & (CURRENT['Selected_Total_Dist'] == 1)]
CURRENT_QUARTILE4 = CURRENT[(CURRENT['HPIQuartile'] == 4) & (CURRENT['Selected_Total_Dist'] == 1)]
DOLLAR_QUARTILE1 = DOLLAR[(DOLLAR['HPIQuartile'] == 1) & (DOLLAR['Selected_Total_Dist'] == 1)]
DOLLAR_QUARTILE2 = DOLLAR[(DOLLAR['HPIQuartile'] == 2) & (DOLLAR['Selected_Total_Dist'] == 1)]
DOLLAR_QUARTILE3 = DOLLAR[(DOLLAR['HPIQuartile'] == 3) & (DOLLAR['Selected_Total_Dist'] == 1)]
DOLLAR_QUARTILE4 = DOLLAR[(DOLLAR['HPIQuartile'] == 4) & (DOLLAR['Selected_Total_Dist'] == 1)]

currenttotal1 = CURRENT_QUARTILE1['Utilization_HPI1_Total_Dist'] +\
    CURRENT_QUARTILE1['Utilization_HPI2_Total_Dist'] +\
        CURRENT_QUARTILE1['Utilization_HPI3_Total_Dist']+\
            CURRENT_QUARTILE1['Utilization_HPI4_Total_Dist']
    
currenttotal2 = CURRENT_QUARTILE2['Utilization_HPI1_Total_Dist'] +\
    CURRENT_QUARTILE2['Utilization_HPI2_Total_Dist'] +\
        CURRENT_QUARTILE2['Utilization_HPI3_Total_Dist']+\
            CURRENT_QUARTILE2['Utilization_HPI4_Total_Dist']
            
currenttotal3 = CURRENT_QUARTILE3['Utilization_HPI1_Total_Dist'] +\
    CURRENT_QUARTILE3['Utilization_HPI2_Total_Dist'] +\
        CURRENT_QUARTILE3['Utilization_HPI3_Total_Dist']+\
            CURRENT_QUARTILE3['Utilization_HPI4_Total_Dist']            
            
currenttotal4 = CURRENT_QUARTILE4['Utilization_HPI1_Total_Dist'] +\
    CURRENT_QUARTILE4['Utilization_HPI2_Total_Dist'] +\
        CURRENT_QUARTILE4['Utilization_HPI3_Total_Dist']+\
            CURRENT_QUARTILE4['Utilization_HPI4_Total_Dist']
            
dollartotal1 = DOLLAR_QUARTILE1['Utilization_HPI1_Total_Dist'] +\
    DOLLAR_QUARTILE1['Utilization_HPI2_Total_Dist'] +\
        DOLLAR_QUARTILE1['Utilization_HPI3_Total_Dist']+\
            DOLLAR_QUARTILE1['Utilization_HPI4_Total_Dist']
    
dollartotal2 = DOLLAR_QUARTILE2['Utilization_HPI1_Total_Dist'] +\
    DOLLAR_QUARTILE2['Utilization_HPI2_Total_Dist'] +\
        DOLLAR_QUARTILE2['Utilization_HPI3_Total_Dist']+\
            DOLLAR_QUARTILE2['Utilization_HPI4_Total_Dist']
            
dollartotal3 = DOLLAR_QUARTILE3['Utilization_HPI1_Total_Dist'] +\
    DOLLAR_QUARTILE3['Utilization_HPI2_Total_Dist'] +\
        DOLLAR_QUARTILE3['Utilization_HPI3_Total_Dist']+\
            DOLLAR_QUARTILE3['Utilization_HPI4_Total_Dist']            
            
dollartotal4 = DOLLAR_QUARTILE4['Utilization_HPI1_Total_Dist'] +\
    DOLLAR_QUARTILE4['Utilization_HPI2_Total_Dist'] +\
        DOLLAR_QUARTILE4['Utilization_HPI3_Total_Dist']+\
            DOLLAR_QUARTILE4['Utilization_HPI4_Total_Dist']

table = np.round(np.array([[np.mean(CURRENT_QUARTILE1['Utilization_HPI1_Total_Dist']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI2_Total_Dist']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI3_Total_Dist']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI4_Total_Dist']),
                            np.mean(currenttotal1),
                            np.mean(DOLLAR_QUARTILE1['Utilization_HPI1_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE1['Utilization_HPI2_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE1['Utilization_HPI3_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE1['Utilization_HPI4_Total_Dist']),
                            np.mean(dollartotal1)],
                           [np.mean(CURRENT_QUARTILE2['Utilization_HPI1_Total_Dist']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI2_Total_Dist']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI3_Total_Dist']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI4_Total_Dist']),
                            np.mean(currenttotal2),
                            np.mean(DOLLAR_QUARTILE2['Utilization_HPI1_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE2['Utilization_HPI2_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE2['Utilization_HPI3_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE2['Utilization_HPI4_Total_Dist']),
                            np.mean(dollartotal2)],
                           [np.mean(CURRENT_QUARTILE3['Utilization_HPI1_Total_Dist']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI2_Total_Dist']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI3_Total_Dist']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI4_Total_Dist']),
                            np.mean(currenttotal3),
                            np.mean(DOLLAR_QUARTILE3['Utilization_HPI1_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE3['Utilization_HPI2_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE3['Utilization_HPI3_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE3['Utilization_HPI4_Total_Dist']),
                            np.mean(dollartotal3)],
                           [np.mean(CURRENT_QUARTILE4['Utilization_HPI1_Total_Dist']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI2_Total_Dist']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI3_Total_Dist']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI4_Total_Dist']),
                            np.mean(currenttotal4),
                            np.mean(DOLLAR_QUARTILE4['Utilization_HPI1_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE4['Utilization_HPI2_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE4['Utilization_HPI3_Total_Dist']),
                            np.mean(DOLLAR_QUARTILE4['Utilization_HPI4_Total_Dist']),
                            np.mean(dollartotal4)]
                           ]) * 100, 2)

print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

table_var = np.round(np.array([[np.var(CURRENT_QUARTILE1['Utilization_HPI1_Total_Dist']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI2_Total_Dist']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI3_Total_Dist']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI4_Total_Dist']),
                            np.var(currenttotal1),
                            np.var(DOLLAR_QUARTILE1['Utilization_HPI1_Total_Dist']),
                            np.var(DOLLAR_QUARTILE1['Utilization_HPI2_Total_Dist']),
                            np.var(DOLLAR_QUARTILE1['Utilization_HPI3_Total_Dist']),
                            np.var(DOLLAR_QUARTILE1['Utilization_HPI4_Total_Dist']),
                            np.var(dollartotal1)],
                           [np.var(CURRENT_QUARTILE2['Utilization_HPI1_Total_Dist']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI2_Total_Dist']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI3_Total_Dist']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI4_Total_Dist']),
                            np.var(currenttotal2),
                            np.var(DOLLAR_QUARTILE2['Utilization_HPI1_Total_Dist']),
                            np.var(DOLLAR_QUARTILE2['Utilization_HPI2_Total_Dist']),
                            np.var(DOLLAR_QUARTILE2['Utilization_HPI3_Total_Dist']),
                            np.var(DOLLAR_QUARTILE2['Utilization_HPI4_Total_Dist']),
                            np.var(dollartotal2)],
                           [np.var(CURRENT_QUARTILE3['Utilization_HPI1_Total_Dist']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI2_Total_Dist']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI3_Total_Dist']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI4_Total_Dist']),
                            np.var(currenttotal3),
                            np.var(DOLLAR_QUARTILE3['Utilization_HPI1_Total_Dist']),
                            np.var(DOLLAR_QUARTILE3['Utilization_HPI2_Total_Dist']),
                            np.var(DOLLAR_QUARTILE3['Utilization_HPI3_Total_Dist']),
                            np.var(DOLLAR_QUARTILE3['Utilization_HPI4_Total_Dist']),
                            np.var(dollartotal3)],
                           [np.var(CURRENT_QUARTILE4['Utilization_HPI1_Total_Dist']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI2_Total_Dist']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI3_Total_Dist']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI4_Total_Dist']),
                            np.var(currenttotal4),
                            np.var(DOLLAR_QUARTILE4['Utilization_HPI1_Total_Dist']),
                            np.var(DOLLAR_QUARTILE4['Utilization_HPI2_Total_Dist']),
                            np.var(DOLLAR_QUARTILE4['Utilization_HPI3_Total_Dist']),
                            np.var(DOLLAR_QUARTILE4['Utilization_HPI4_Total_Dist']),
                            np.var(dollartotal4)]
                           ]) * 100, 1)

print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))


### Total + DistHPI
CURRENT_QUARTILE1 = CURRENT[(CURRENT['HPIQuartile'] == 1) & (CURRENT['Selected_Total_DistHPI'] == 1)]
CURRENT_QUARTILE2 = CURRENT[(CURRENT['HPIQuartile'] == 2) & (CURRENT['Selected_Total_DistHPI'] == 1)]
CURRENT_QUARTILE3 = CURRENT[(CURRENT['HPIQuartile'] == 3) & (CURRENT['Selected_Total_DistHPI'] == 1)]
CURRENT_QUARTILE4 = CURRENT[(CURRENT['HPIQuartile'] == 4) & (CURRENT['Selected_Total_DistHPI'] == 1)]
DOLLAR_QUARTILE1 = DOLLAR[(DOLLAR['HPIQuartile'] == 1) & (DOLLAR['Selected_Total_DistHPI'] == 1)]
DOLLAR_QUARTILE2 = DOLLAR[(DOLLAR['HPIQuartile'] == 2) & (DOLLAR['Selected_Total_DistHPI'] == 1)]
DOLLAR_QUARTILE3 = DOLLAR[(DOLLAR['HPIQuartile'] == 3) & (DOLLAR['Selected_Total_DistHPI'] == 1)]
DOLLAR_QUARTILE4 = DOLLAR[(DOLLAR['HPIQuartile'] == 4) & (DOLLAR['Selected_Total_DistHPI'] == 1)]

currenttotal1 = CURRENT_QUARTILE1['Utilization_HPI1_Total_DistHPI'] +\
    CURRENT_QUARTILE1['Utilization_HPI2_Total_DistHPI'] +\
        CURRENT_QUARTILE1['Utilization_HPI3_Total_DistHPI']+\
            CURRENT_QUARTILE1['Utilization_HPI4_Total_DistHPI']
    
currenttotal2 = CURRENT_QUARTILE2['Utilization_HPI1_Total_DistHPI'] +\
    CURRENT_QUARTILE2['Utilization_HPI2_Total_DistHPI'] +\
        CURRENT_QUARTILE2['Utilization_HPI3_Total_DistHPI']+\
            CURRENT_QUARTILE2['Utilization_HPI4_Total_DistHPI']
            
currenttotal3 = CURRENT_QUARTILE3['Utilization_HPI1_Total_DistHPI'] +\
    CURRENT_QUARTILE3['Utilization_HPI2_Total_DistHPI'] +\
        CURRENT_QUARTILE3['Utilization_HPI3_Total_DistHPI']+\
            CURRENT_QUARTILE3['Utilization_HPI4_Total_DistHPI']            
            
currenttotal4 = CURRENT_QUARTILE4['Utilization_HPI1_Total_DistHPI'] +\
    CURRENT_QUARTILE4['Utilization_HPI2_Total_DistHPI'] +\
        CURRENT_QUARTILE4['Utilization_HPI3_Total_DistHPI']+\
            CURRENT_QUARTILE4['Utilization_HPI4_Total_DistHPI']
            
dollartotal1 = DOLLAR_QUARTILE1['Utilization_HPI1_Total_DistHPI'] +\
    DOLLAR_QUARTILE1['Utilization_HPI2_Total_DistHPI'] +\
        DOLLAR_QUARTILE1['Utilization_HPI3_Total_DistHPI']+\
            DOLLAR_QUARTILE1['Utilization_HPI4_Total_DistHPI']
    
dollartotal2 = DOLLAR_QUARTILE2['Utilization_HPI1_Total_DistHPI'] +\
    DOLLAR_QUARTILE2['Utilization_HPI2_Total_DistHPI'] +\
        DOLLAR_QUARTILE2['Utilization_HPI3_Total_DistHPI']+\
            DOLLAR_QUARTILE2['Utilization_HPI4_Total_DistHPI']
            
dollartotal3 = DOLLAR_QUARTILE3['Utilization_HPI1_Total_DistHPI'] +\
    DOLLAR_QUARTILE3['Utilization_HPI2_Total_DistHPI'] +\
        DOLLAR_QUARTILE3['Utilization_HPI3_Total_DistHPI']+\
            DOLLAR_QUARTILE3['Utilization_HPI4_Total_DistHPI']            
            
dollartotal4 = DOLLAR_QUARTILE4['Utilization_HPI1_Total_DistHPI'] +\
    DOLLAR_QUARTILE4['Utilization_HPI2_Total_DistHPI'] +\
        DOLLAR_QUARTILE4['Utilization_HPI3_Total_DistHPI']+\
            DOLLAR_QUARTILE4['Utilization_HPI4_Total_DistHPI']

table = np.round(np.array([[np.mean(CURRENT_QUARTILE1['Utilization_HPI1_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI2_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI3_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE1['Utilization_HPI4_Total_DistHPI']),
                            np.mean(currenttotal1),
                            np.mean(DOLLAR_QUARTILE1['Utilization_HPI1_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE1['Utilization_HPI2_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE1['Utilization_HPI3_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE1['Utilization_HPI4_Total_DistHPI']),
                            np.mean(dollartotal1)],
                           [np.mean(CURRENT_QUARTILE2['Utilization_HPI1_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI2_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI3_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE2['Utilization_HPI4_Total_DistHPI']),
                            np.mean(currenttotal2),
                            np.mean(DOLLAR_QUARTILE2['Utilization_HPI1_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE2['Utilization_HPI2_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE2['Utilization_HPI3_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE2['Utilization_HPI4_Total_DistHPI']),
                            np.mean(dollartotal2)],
                           [np.mean(CURRENT_QUARTILE3['Utilization_HPI1_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI2_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI3_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE3['Utilization_HPI4_Total_DistHPI']),
                            np.mean(currenttotal3),
                            np.mean(DOLLAR_QUARTILE3['Utilization_HPI1_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE3['Utilization_HPI2_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE3['Utilization_HPI3_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE3['Utilization_HPI4_Total_DistHPI']),
                            np.mean(dollartotal3)],
                           [np.mean(CURRENT_QUARTILE4['Utilization_HPI1_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI2_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI3_Total_DistHPI']),
                            np.mean(CURRENT_QUARTILE4['Utilization_HPI4_Total_DistHPI']),
                            np.mean(currenttotal4),
                            np.mean(DOLLAR_QUARTILE4['Utilization_HPI1_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE4['Utilization_HPI2_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE4['Utilization_HPI3_Total_DistHPI']),
                            np.mean(DOLLAR_QUARTILE4['Utilization_HPI4_Total_DistHPI']),
                            np.mean(dollartotal4)]
                           ]) * 100, 2)

print(tabulate(table, tablefmt="latex", floatfmt=".2f"))

table_var = np.round(np.array([[np.var(CURRENT_QUARTILE1['Utilization_HPI1_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI2_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI3_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE1['Utilization_HPI4_Total_DistHPI']),
                            np.var(currenttotal1),
                            np.var(DOLLAR_QUARTILE1['Utilization_HPI1_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE1['Utilization_HPI2_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE1['Utilization_HPI3_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE1['Utilization_HPI4_Total_DistHPI']),
                            np.var(dollartotal1)],
                           [np.var(CURRENT_QUARTILE2['Utilization_HPI1_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI2_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI3_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE2['Utilization_HPI4_Total_DistHPI']),
                            np.var(currenttotal2),
                            np.var(DOLLAR_QUARTILE2['Utilization_HPI1_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE2['Utilization_HPI2_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE2['Utilization_HPI3_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE2['Utilization_HPI4_Total_DistHPI']),
                            np.var(dollartotal2)],
                           [np.var(CURRENT_QUARTILE3['Utilization_HPI1_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI2_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI3_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE3['Utilization_HPI4_Total_DistHPI']),
                            np.var(currenttotal3),
                            np.var(DOLLAR_QUARTILE3['Utilization_HPI1_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE3['Utilization_HPI2_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE3['Utilization_HPI3_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE3['Utilization_HPI4_Total_DistHPI']),
                            np.var(dollartotal3)],
                           [np.var(CURRENT_QUARTILE4['Utilization_HPI1_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI2_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI3_Total_DistHPI']),
                            np.var(CURRENT_QUARTILE4['Utilization_HPI4_Total_DistHPI']),
                            np.var(currenttotal4),
                            np.var(DOLLAR_QUARTILE4['Utilization_HPI1_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE4['Utilization_HPI2_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE4['Utilization_HPI3_Total_DistHPI']),
                            np.var(DOLLAR_QUARTILE4['Utilization_HPI4_Total_DistHPI']),
                            np.var(dollartotal4)]
                           ]) * 100, 1)

print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))


###########################################################################

### Utilization rate of N stores nearby (unscaled)

CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]

table_mean = np.round(np.array([[np.mean(CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Current_Dist']),0],
                       [np.mean(CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Current_Dist']),0],
                       [np.mean(CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Current_Dist']),0],
                       [np.mean(CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Current_Dist']),0],
                       [np.mean(CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.mean(CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.mean(CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.mean(CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.mean(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Pharmacy_Nearby_Total_Dist']),
                        np.mean(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Dollar_Nearby_Total_Dist'])],
                       [np.mean(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Pharmacy_Nearby_Total_Dist']),
                        np.mean(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Dollar_Nearby_Total_Dist'])],
                       [np.mean(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Pharmacy_Nearby_Total_Dist']),
                        np.mean(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Dollar_Nearby_Total_Dist'])],
                       [np.mean(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Pharmacy_Nearby_Total_Dist']),
                        np.mean(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Dollar_Nearby_Total_Dist'])],
                       [np.mean(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Pharmacy_Nearby_Total_DistHPI']),
                        np.mean(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Dollar_Nearby_Total_DistHPI'])],
                       [np.mean(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Pharmacy_Nearby_Total_DistHPI']),
                        np.mean(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Dollar_Nearby_Total_DistHPI'])],
                       [np.mean(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Pharmacy_Nearby_Total_DistHPI']),
                        np.mean(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Dollar_Nearby_Total_DistHPI'])],
                       [np.mean(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Pharmacy_Nearby_Total_DistHPI']),
                        np.mean(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Dollar_Nearby_Total_DistHPI'])]]) * 100, 2)
                      
print(tabulate(table_mean, tablefmt="latex", floatfmt=".2f"))


table_var = np.round(np.array([[np.var(CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Current_Dist']),0],
                       [np.var(CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Current_Dist']),0],
                       [np.var(CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Current_Dist']),0],
                       [np.var(CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Current_Dist']),0],
                       [np.var(CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.var(CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.var(CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.var(CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.var(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Pharmacy_Nearby_Total_Dist']),
                        np.var(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Dollar_Nearby_Total_Dist'])],
                       [np.var(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Pharmacy_Nearby_Total_Dist']),
                        np.var(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Dollar_Nearby_Total_Dist'])],
                       [np.var(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Pharmacy_Nearby_Total_Dist']),
                        np.var(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Dollar_Nearby_Total_Dist'])],
                       [np.var(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Pharmacy_Nearby_Total_Dist']),
                        np.var(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Dollar_Nearby_Total_Dist'])],
                       [np.var(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Pharmacy_Nearby_Total_DistHPI']),
                        np.var(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Dollar_Nearby_Total_DistHPI'])],
                       [np.var(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Pharmacy_Nearby_Total_DistHPI']),
                        np.var(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Dollar_Nearby_Total_DistHPI'])],
                       [np.var(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Pharmacy_Nearby_Total_DistHPI']),
                        np.var(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Dollar_Nearby_Total_DistHPI'])],
                       [np.var(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Pharmacy_Nearby_Total_DistHPI']),
                        np.var(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Dollar_Nearby_Total_DistHPI'])]]) * 100, 2)
                      
print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))

table_mean = np.round(np.array([[np.mean(CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Total_Dist']+\
                              CA_TRACT_QUARTILE1['Utilization_Dollar_Nearby_Total_Dist'])],
                      [np.mean(CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Total_Dist']+\
                              CA_TRACT_QUARTILE2['Utilization_Dollar_Nearby_Total_Dist'])],
                          [np.mean(CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Total_Dist']+\
                                  CA_TRACT_QUARTILE3['Utilization_Dollar_Nearby_Total_Dist'])],
                              [np.mean(CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Total_Dist']+\
                                      CA_TRACT_QUARTILE4['Utilization_Dollar_Nearby_Total_Dist'])]])*100, 2)
                      
print(tabulate(table_mean, tablefmt="latex", floatfmt=".2f"))

table_mean = np.round(np.array([[np.mean(CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Total_DistHPI']+\
                              CA_TRACT_QUARTILE1['Utilization_Dollar_Nearby_Total_DistHPI'])],
                      [np.mean(CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Total_DistHPI']+\
                              CA_TRACT_QUARTILE2['Utilization_Dollar_Nearby_Total_DistHPI'])],
                          [np.mean(CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Total_DistHPI']+\
                                  CA_TRACT_QUARTILE3['Utilization_Dollar_Nearby_Total_DistHPI'])],
                              [np.mean(CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Total_DistHPI']+\
                                      CA_TRACT_QUARTILE4['Utilization_Dollar_Nearby_Total_DistHPI'])]])*100, 2)
                      
print(tabulate(table_mean, tablefmt="latex", floatfmt=".2f"))

table_var = np.round(np.array([[np.var(CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Total_Dist']+\
                              CA_TRACT_QUARTILE1['Utilization_Dollar_Nearby_Total_Dist'])],
                      [np.var(CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Total_Dist']+\
                              CA_TRACT_QUARTILE2['Utilization_Dollar_Nearby_Total_Dist'])],
                          [np.var(CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Total_Dist']+\
                                  CA_TRACT_QUARTILE3['Utilization_Dollar_Nearby_Total_Dist'])],
                              [np.var(CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Total_Dist']+\
                                      CA_TRACT_QUARTILE4['Utilization_Dollar_Nearby_Total_Dist'])]])*100, 2)
                      
print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))

table_var = np.round(np.array([[np.var(CA_TRACT_QUARTILE1['Utilization_Pharmacy_Nearby_Total_DistHPI']+\
                              CA_TRACT_QUARTILE1['Utilization_Dollar_Nearby_Total_DistHPI'])],
                      [np.var(CA_TRACT_QUARTILE2['Utilization_Pharmacy_Nearby_Total_DistHPI']+\
                              CA_TRACT_QUARTILE2['Utilization_Dollar_Nearby_Total_DistHPI'])],
                          [np.var(CA_TRACT_QUARTILE3['Utilization_Pharmacy_Nearby_Total_DistHPI']+\
                                  CA_TRACT_QUARTILE3['Utilization_Dollar_Nearby_Total_DistHPI'])],
                              [np.var(CA_TRACT_QUARTILE4['Utilization_Pharmacy_Nearby_Total_DistHPI']+\
                                      CA_TRACT_QUARTILE4['Utilization_Dollar_Nearby_Total_DistHPI'])]])*100, 2)
                      
print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))


###########################################################################

### Utilization rate of N stores nearby (scaled)



total_dist = np.sum(np.multiply(F_DH_total, mat_y_total), axis = 1)
total_distHPI = np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1)
CA_TRACT['Utilization_Scaled_All_Nearby_Total_Dist'] = (CA_TRACT['Utilization_Pharmacy_Nearby_Total_Dist'] + CA_TRACT['Utilization_Dollar_Nearby_Total_Dist']) / total_dist
CA_TRACT['Utilization_Scaled_All_Nearby_Total_DistHPI'] = (CA_TRACT['Utilization_Pharmacy_Nearby_Total_DistHPI'] + CA_TRACT['Utilization_Dollar_Nearby_Total_DistHPI']) / total_distHPI

CA_TRACT_QUARTILE1 = CA_TRACT[CA_TRACT['HPIQuartile'] == 1]
CA_TRACT_QUARTILE2 = CA_TRACT[CA_TRACT['HPIQuartile'] == 2]
CA_TRACT_QUARTILE3 = CA_TRACT[CA_TRACT['HPIQuartile'] == 3]
CA_TRACT_QUARTILE4 = CA_TRACT[CA_TRACT['HPIQuartile'] == 4]


table_mean = np.round(np.array([[np.mean(CA_TRACT_QUARTILE1['Utilization_Scaled_Pharmacy_Nearby_Current_Dist']),0],
                       [np.mean(CA_TRACT_QUARTILE2['Utilization_Scaled_Pharmacy_Nearby_Current_Dist']),0],
                       [np.mean(CA_TRACT_QUARTILE3['Utilization_Scaled_Pharmacy_Nearby_Current_Dist']),0],
                       [np.mean(CA_TRACT_QUARTILE4['Utilization_Scaled_Pharmacy_Nearby_Current_Dist']),0],
                       [np.mean(CA_TRACT_QUARTILE1['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.mean(CA_TRACT_QUARTILE2['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.mean(CA_TRACT_QUARTILE3['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.mean(CA_TRACT_QUARTILE4['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.mean(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_Dist']),
                        np.mean(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Scaled_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_Dist'])],
                       [np.mean(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_Dist']),
                        np.mean(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Scaled_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_Dist'])],
                       [np.mean(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_Dist']),
                        np.mean(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Scaled_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_Dist'])],
                       [np.mean(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_Dist']),
                        np.mean(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Scaled_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_Dist'])],
                       [np.mean(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI']),
                        np.mean(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'])],
                       [np.mean(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI']),
                        np.mean(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'])],
                       [np.mean(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI']),
                        np.mean(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'])],
                       [np.mean(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI']),
                        np.mean(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'])]])*100, 2)
                      
print(tabulate(table_mean, tablefmt="latex", floatfmt=".2f"))


table_var = np.round(np.array([[np.var(CA_TRACT_QUARTILE1['Utilization_Scaled_Pharmacy_Nearby_Current_Dist']),0],
                       [np.var(CA_TRACT_QUARTILE2['Utilization_Scaled_Pharmacy_Nearby_Current_Dist']),0],
                       [np.var(CA_TRACT_QUARTILE3['Utilization_Scaled_Pharmacy_Nearby_Current_Dist']),0],
                       [np.var(CA_TRACT_QUARTILE4['Utilization_Scaled_Pharmacy_Nearby_Current_Dist']),0],
                       [np.var(CA_TRACT_QUARTILE1['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.var(CA_TRACT_QUARTILE2['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.var(CA_TRACT_QUARTILE3['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.var(CA_TRACT_QUARTILE4['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI']),0],
                       [np.var(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_Dist']),
                        np.var(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Scaled_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_Dist'])],
                       [np.var(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_Dist']),
                        np.var(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Scaled_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_Dist'])],
                       [np.var(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_Dist']),
                        np.var(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Scaled_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_Dist'])],
                       [np.var(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_Dist']),
                        np.var(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Scaled_Dollar_Nearby_Total_Dist'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_Dist'])],
                       [np.var(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI']),
                        np.var(CA_TRACT_QUARTILE1[CA_TRACT_QUARTILE1['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'])],
                       [np.var(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI']),
                        np.var(CA_TRACT_QUARTILE2[CA_TRACT_QUARTILE2['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'])],
                       [np.var(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI']),
                        np.var(CA_TRACT_QUARTILE3[CA_TRACT_QUARTILE3['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'])],
                       [np.var(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI']),
                        np.var(CA_TRACT_QUARTILE4[CA_TRACT_QUARTILE4['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] != 0]['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'])]])*100, 2)
                      
print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))



table_mean = np.round(np.array([[np.mean(CA_TRACT_QUARTILE1['Utilization_Scaled_All_Nearby_Total_Dist'])],
                                [np.mean(CA_TRACT_QUARTILE2['Utilization_Scaled_All_Nearby_Total_Dist'])],
                                [np.mean(CA_TRACT_QUARTILE3['Utilization_Scaled_All_Nearby_Total_Dist'])],
                                [np.mean(CA_TRACT_QUARTILE4['Utilization_Scaled_All_Nearby_Total_Dist'])],
                                [np.mean(CA_TRACT_QUARTILE1['Utilization_Scaled_All_Nearby_Total_DistHPI'])],
                                [np.mean(CA_TRACT_QUARTILE2['Utilization_Scaled_All_Nearby_Total_DistHPI'])],
                                [np.mean(CA_TRACT_QUARTILE3['Utilization_Scaled_All_Nearby_Total_DistHPI'])],
                                [np.mean(CA_TRACT_QUARTILE4['Utilization_Scaled_All_Nearby_Total_DistHPI'])]]) * 100, 2)
                      
print(tabulate(table_mean, tablefmt="latex", floatfmt=".2f"))

table_var = np.round(np.array([[np.var(CA_TRACT_QUARTILE1['Utilization_Scaled_All_Nearby_Total_Dist'])],
                                [np.var(CA_TRACT_QUARTILE2['Utilization_Scaled_All_Nearby_Total_Dist'])],
                                [np.var(CA_TRACT_QUARTILE3['Utilization_Scaled_All_Nearby_Total_Dist'])],
                                [np.var(CA_TRACT_QUARTILE4['Utilization_Scaled_All_Nearby_Total_Dist'])],
                                [np.var(CA_TRACT_QUARTILE1['Utilization_Scaled_All_Nearby_Total_DistHPI'])],
                                [np.var(CA_TRACT_QUARTILE2['Utilization_Scaled_All_Nearby_Total_DistHPI'])],
                                [np.var(CA_TRACT_QUARTILE3['Utilization_Scaled_All_Nearby_Total_DistHPI'])],
                                [np.var(CA_TRACT_QUARTILE4['Utilization_Scaled_All_Nearby_Total_DistHPI'])]]) * 100, 2)
                      
print(tabulate(table_var, tablefmt="latex", floatfmt=".1f"))





