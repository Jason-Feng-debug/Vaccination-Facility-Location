#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30, 2022
@Author: Jingyuan Hu

INPUT: Optimal solution
OUTPUT: Rate, distance for each quartile
"""

import os
import pandas as pd
import numpy as np

os.chdir('/Users/jingyuanhu/Desktop/Research/COVID_project/Submission MS/Code')

###########################################################################

### Zip code ###

# CA_ZIP = pd.read_csv('../Data/CaliforniaZipHPI.csv', delimiter = ",") 
# Population = CA_ZIP['Population'].values
# total_population = sum(Population)
# Quartile = CA_ZIP['HPIQuartile'].values.astype(int)

# population1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Population'].values)
# population2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Population'].values)
# population3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Population'].values)
# population4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Population'].values)

# population_vec = [total_population, population1, population2, population3, population4]

# C_current = np.genfromtxt('../Data/dist_matrix_CA_current.csv', delimiter = ",", dtype = float)
# C_current = C_current.astype(int)
# C_current = C_current.T
# num_zips, num_current_stores = np.shape(C_current)
# closest_dist_current = np.min(C_current, axis = 1)
# CA_ZIP['Closest_Dist_Current'] = closest_dist_current

# C_dollar = np.genfromtxt('../Data/dist_matrix_CA_dollar.csv', delimiter = ",", dtype = float)
# C_dollar = C_dollar.astype(int)
# C_dollar = C_dollar.T
# num_zips, num_dollar_stores = np.shape(C_dollar)

# C_total = np.concatenate((C_current, C_dollar), axis = 1)
# num_total_stores = num_current_stores + num_dollar_stores
# closest_dist_total = np.min(C_total, axis = 1)
# CA_ZIP['Closest_Dist_Total'] = closest_dist_total

###########################################################################

### Census Tract ###

Population = np.genfromtxt('../Data/population_tract.csv', delimiter = ",", dtype = int)
total_population = sum(Population)
Quartile = np.genfromtxt('../Data/quartile_tract.csv', delimiter = ",", dtype = int)
CA_ZIP = pd.DataFrame(data = {'Population': Population, 'HPIQuartile': Quartile})

population1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Population'].values)
population2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Population'].values)
population3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Population'].values)
population4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Population'].values)

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

# Import solution
y_current = np.genfromtxt('../Result/Tract_0.84capacity_N20/Dist/y_current.csv', delimiter = ",", dtype = float)
y_current_hpi = np.genfromtxt('../Result/Tract_0.84capacity_N20/HPI_Dist/y_current.csv', delimiter = ",", dtype = float)
y_total = np.genfromtxt('../Result/Tract_0.84capacity_N20/Dist/y_total.csv', delimiter = ",", dtype = float)
y_total_hpi = np.genfromtxt('../Result/Tract_0.84capacity_N20/HPI_Dist/y_total.csv', delimiter = ",", dtype = float)

# Zip
y_current = np.genfromtxt('../Result/Zip/Dist/y_current.csv', delimiter = ",", dtype = float)
y_current_hpi = np.genfromtxt('../Result/Zip/HPI_Dist/y_current.csv', delimiter = ",", dtype = float)
y_total = np.genfromtxt('../Result/Zip/Dist/y_total.csv', delimiter = ",", dtype = float)
y_total_hpi = np.genfromtxt('../Result/Zip/HPI_Dist/y_total.csv', delimiter = ",", dtype = float)

# Tract
y_current = np.genfromtxt('../Result/Tract/Dist/y_current.csv', delimiter = ",", dtype = float)
y_current_hpi = np.genfromtxt('../Result/Tract/HPI_Dist/y_current.csv', delimiter = ",", dtype = float)
y_total = np.genfromtxt('../Result/Tract/Dist/y_total.csv', delimiter = ",", dtype = float)
y_total_hpi = np.genfromtxt('../Result/Tract/HPI_Dist/y_total.csv', delimiter = ",", dtype = float)

mat_y_current = np.reshape(y_current, (num_zips, num_current_stores))
mat_y_current_hpi = np.reshape(y_current_hpi, (num_zips, num_current_stores))
mat_y_total = np.reshape(y_total, (num_zips, num_total_stores))
mat_y_total_hpi = np.reshape(y_total_hpi, (num_zips, num_total_stores))


###########################################################################

### Vaccination rate for each quartile
rate_current = np.sum(np.multiply(F_DH_current, mat_y_current), axis = 1)
rate_current_hpi = np.sum(np.multiply(F_DH_current, mat_y_current_hpi), axis = 1)
rate_total = np.sum(np.multiply(F_DH_total, mat_y_total), axis = 1)
rate_total_hpi = np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1)

CA_ZIP['Rate_Current'] = rate_current
CA_ZIP['Rate_Current_HPI'] = rate_current_hpi
CA_ZIP['Rate_Total'] = rate_total
CA_ZIP['Rate_Total_HPI'] = rate_total_hpi

CA_ZIP['Rate_Current_weighted'] = CA_ZIP['Rate_Current'] * CA_ZIP['Population']
CA_ZIP['Rate_Current_HPI_weighted'] = CA_ZIP['Rate_Current_HPI'] * CA_ZIP['Population']
CA_ZIP['Rate_Total_weighted'] = CA_ZIP['Rate_Total'] * CA_ZIP['Population']
CA_ZIP['Rate_Total_HPI_weighted'] = CA_ZIP['Rate_Total_HPI'] * CA_ZIP['Population']


rate_current = sum(CA_ZIP['Rate_Current_weighted'].values) / total_population
rate_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Rate_Current_weighted'].values) / population1
rate_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Rate_Current_weighted'].values) / population2
rate_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Rate_Current_weighted'].values) / population3
rate_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Rate_Current_weighted'].values) / population4

rate_current_hpi = sum(CA_ZIP['Rate_Current_HPI_weighted'].values) / total_population
rate_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Rate_Current_HPI_weighted'].values) / population1
rate_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Rate_Current_HPI_weighted'].values) / population2
rate_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Rate_Current_HPI_weighted'].values) / population3
rate_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Rate_Current_HPI_weighted'].values) / population4

rate_total = sum(CA_ZIP['Rate_Total_weighted'].values) / total_population
rate_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Rate_Total_weighted'].values) / population1
rate_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Rate_Total_weighted'].values) / population2
rate_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Rate_Total_weighted'].values) / population3
rate_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Rate_Total_weighted'].values) / population4

rate_total_hpi = sum(CA_ZIP['Rate_Total_HPI_weighted'].values) / total_population
rate_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Rate_Total_HPI_weighted'].values) / population1
rate_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Rate_Total_HPI_weighted'].values) / population2
rate_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Rate_Total_HPI_weighted'].values) / population3
rate_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Rate_Total_HPI_weighted'].values) / population4

# rate = np.array([[rate_current, rate_current1, rate_current2, rate_current3, rate_current4],
#                   [rate_current_hpi, rate_current_hpi1, rate_current_hpi2, rate_current_hpi3, rate_current_hpi4]
#                   ])

rate = np.array([[rate_current, rate_current1, rate_current2, rate_current3, rate_current4],
                 [rate_current_hpi, rate_current_hpi1, rate_current_hpi2, rate_current_hpi3, rate_current_hpi4],
                 [rate_total, rate_total1, rate_total2, rate_total3, rate_total4],
                 [rate_total_hpi, rate_total_hpi1, rate_total_hpi2, rate_total_hpi3, rate_total_hpi4]
                 ])

# np.round(rate,4) * 100
# np.round(rate * population_vec / 1000000,2)
# Vaccinated rate and population
np.concatenate((np.round(rate,4) * 100, np.round(rate * population_vec / 1000000,2)), axis=1)

###########################################################################

### Average distance for each quartile
avg_dist_current = np.round(np.sum(np.multiply(C_current, mat_y_current), axis = 1),1)
avg_dist_current_hpi = np.round(np.sum(np.multiply(C_current, mat_y_current_hpi), axis = 1),1)
avg_dist_total = np.round(np.sum(np.multiply(C_total, mat_y_total), axis = 1),1)
avg_dist_total_hpi = np.round(np.sum(np.multiply(C_total, mat_y_total_hpi), axis = 1),1)

CA_ZIP['Dist_Current'] = avg_dist_current
CA_ZIP['Dist_Current_HPI'] = avg_dist_current_hpi
CA_ZIP['Dist_Total'] = avg_dist_total
CA_ZIP['Dist_Total_HPI'] = avg_dist_total_hpi

CA_ZIP['Dist_Current_weighted'] = CA_ZIP['Dist_Current'] * CA_ZIP['Population']
CA_ZIP['Dist_Current_HPI_weighted'] = CA_ZIP['Dist_Current_HPI'] * CA_ZIP['Population']
CA_ZIP['Dist_Total_weighted'] = CA_ZIP['Dist_Total'] * CA_ZIP['Population']
CA_ZIP['Dist_Total_HPI_weighted'] = CA_ZIP['Dist_Total_HPI'] * CA_ZIP['Population']

avg_dist_current = sum(CA_ZIP['Dist_Current_weighted'].values) / total_population
avg_dist_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Current_weighted'].values) / population1
avg_dist_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Current_weighted'].values) / population2
avg_dist_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Current_weighted'].values) / population3
avg_dist_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Current_weighted'].values) / population4

avg_dist_current_hpi = sum(CA_ZIP['Dist_Current_HPI_weighted'].values) / total_population
avg_dist_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Current_HPI_weighted'].values) / population1
avg_dist_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Current_HPI_weighted'].values) / population2
avg_dist_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Current_HPI_weighted'].values) / population3
avg_dist_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Current_HPI_weighted'].values) / population4

avg_dist_total = sum(CA_ZIP['Dist_Total_weighted'].values) / total_population
avg_dist_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_weighted'].values) / population1
avg_dist_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_weighted'].values) / population2
avg_dist_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_weighted'].values) / population3
avg_dist_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_weighted'].values) / population4

avg_dist_total_hpi = sum(CA_ZIP['Dist_Total_HPI_weighted'].values) / total_population
avg_dist_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / population1
avg_dist_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / population2
avg_dist_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / population3
avg_dist_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / population4

# avg_dist = np.array([[avg_dist_current, avg_dist_current1, avg_dist_current2, avg_dist_current3, avg_dist_current4],
#                      [avg_dist_current_hpi, avg_dist_current_hpi1, avg_dist_current_hpi2, avg_dist_current_hpi3, avg_dist_current_hpi4]
#                      ])

avg_dist = np.array([[avg_dist_current, avg_dist_current1, avg_dist_current2, avg_dist_current3, avg_dist_current4],
                     [avg_dist_current_hpi, avg_dist_current_hpi1, avg_dist_current_hpi2, avg_dist_current_hpi3, avg_dist_current_hpi4],
                     [avg_dist_total, avg_dist_total1, avg_dist_total2, avg_dist_total3, avg_dist_total4],
                     [avg_dist_total_hpi, avg_dist_total_hpi1, avg_dist_total_hpi2, avg_dist_total_hpi3, avg_dist_total_hpi4]
                     ])

###########################################################################

### Actual distance for each quartile

# avg_dist_current = np.round(np.sum(np.multiply(F_D_current, np.multiply(C_current, mat_y_current)), axis = 1),1)
# avg_dist_current_hpi = np.round(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current_hpi)), axis = 1),1)
# avg_dist_total = np.round(np.sum(np.multiply(F_D_total, np.multiply(C_total, mat_y_total)), axis = 1),1)
# avg_dist_total_hpi = np.round(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1),1)

avg_dist_current = np.round(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current)), axis = 1),1)
avg_dist_current_hpi = np.round(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current_hpi)), axis = 1),1)
avg_dist_total = np.round(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total)), axis = 1),1)
avg_dist_total_hpi = np.round(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1),1)

CA_ZIP['Dist_Current_Actual'] = avg_dist_current
CA_ZIP['Dist_Current_HPI_Actual'] = avg_dist_current_hpi
CA_ZIP['Dist_Total_Actual'] = avg_dist_total
CA_ZIP['Dist_Total_HPI_Actual'] = avg_dist_total_hpi

CA_ZIP['Dist_Current_weighted'] = CA_ZIP['Dist_Current_Actual'] * CA_ZIP['Population']
CA_ZIP['Dist_Current_HPI_weighted'] = CA_ZIP['Dist_Current_HPI_Actual'] * CA_ZIP['Population']
CA_ZIP['Dist_Total_weighted'] = CA_ZIP['Dist_Total_Actual'] * CA_ZIP['Population']
CA_ZIP['Dist_Total_HPI_weighted'] = CA_ZIP['Dist_Total_HPI_Actual'] * CA_ZIP['Population']

avg_dist_current = sum(CA_ZIP['Dist_Current_weighted'].values) / total_population
avg_dist_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Current_weighted'].values) / population1
avg_dist_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Current_weighted'].values) / population2
avg_dist_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Current_weighted'].values) / population3
avg_dist_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Current_weighted'].values) / population4

avg_dist_current_hpi = sum(CA_ZIP['Dist_Current_HPI_weighted'].values) / total_population
avg_dist_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Current_HPI_weighted'].values) / population1
avg_dist_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Current_HPI_weighted'].values) / population2
avg_dist_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Current_HPI_weighted'].values) / population3
avg_dist_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Current_HPI_weighted'].values) / population4

avg_dist_total = sum(CA_ZIP['Dist_Total_weighted'].values) / total_population
avg_dist_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_weighted'].values) / population1
avg_dist_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_weighted'].values) / population2
avg_dist_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_weighted'].values) / population3
avg_dist_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_weighted'].values) / population4

avg_dist_total_hpi = sum(CA_ZIP['Dist_Total_HPI_weighted'].values) / total_population
avg_dist_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / population1
avg_dist_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / population2
avg_dist_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / population3
avg_dist_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / population4

# avg_dist_actual = np.array([[avg_dist_current, avg_dist_current1, avg_dist_current2, avg_dist_current3, avg_dist_current4],
#                             [avg_dist_current_hpi, avg_dist_current_hpi1, avg_dist_current_hpi2, avg_dist_current_hpi3, avg_dist_current_hpi4]
#                             ])

avg_dist_actual = np.array([[avg_dist_current, avg_dist_current1, avg_dist_current2, avg_dist_current3, avg_dist_current4],
                            [avg_dist_current_hpi, avg_dist_current_hpi1, avg_dist_current_hpi2, avg_dist_current_hpi3, avg_dist_current_hpi4],
                            [avg_dist_total, avg_dist_total1, avg_dist_total2, avg_dist_total3, avg_dist_total4],
                            [avg_dist_total_hpi, avg_dist_total_hpi1, avg_dist_total_hpi2, avg_dist_total_hpi3, avg_dist_total_hpi4]
                            ])

###########################################################################

avg_dist = np.round(avg_dist)
avg_dist_actual = np.round(avg_dist_actual)
np.concatenate((avg_dist, avg_dist_actual), axis=1)

###########################################################################

CA_ZIP.to_csv('../Result/CA.csv', index = False)