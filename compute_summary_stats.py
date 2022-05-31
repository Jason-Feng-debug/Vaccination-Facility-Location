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
from tabulate import tabulate

os.chdir('/Users/jingyuanhu/Desktop/Research/COVID project/Submission MS/Code')

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
CA_TRACT = pd.read_csv('../Data/Tract_CA.csv', delimiter = ",")
Population = np.genfromtxt('../Data/population_tract.csv', delimiter = ",", dtype = int)
total_population = sum(Population)
Quartile = np.genfromtxt('../Data/quartile_tract.csv', delimiter = ",", dtype = int)
CA_ZIP = pd.DataFrame(data = {'FIPS': CA_TRACT['FIPS'].values, 'County': CA_TRACT['County_name'].values,
                              'Population': Population, 'HPIQuartile': Quartile})

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

### Walkable distance
C_current_walkable = np.where(C_current < 1000, 1, 0)
C_dollar_walkable = np.where(C_dollar < 1000, 1, 0)
C_total_walkable = np.where(C_total < 1000, 1, 0)

### Vaccine desert (30km)
C_current_desert = np.where(C_current > 30000, 1, 0)
C_dollar_desert = np.where(C_dollar > 30000, 1, 0)
C_total_desert = np.where(C_total > 30000, 1, 0)

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
# path = '../Result/Tract_0.7capacity_N20/'
path = '../Result/Other/Tract_0.84capacity_N20/'

y_current = np.genfromtxt(path + 'Dist/y_current.csv', delimiter = ",", dtype = float)
y_current_hpi = np.genfromtxt(path + 'HPI_Dist/y_current.csv', delimiter = ",", dtype = float)
y_total = np.genfromtxt(path + 'Dist/y_total.csv', delimiter = ",", dtype = float)
y_total_hpi = np.genfromtxt(path + 'HPI_Dist/y_total.csv', delimiter = ",", dtype = float)

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

CA_ZIP['Vaccinated_Population_Current'] = CA_ZIP['Rate_Current'] * CA_ZIP['Population']
CA_ZIP['Vaccinated_Population_Current_HPI'] = CA_ZIP['Rate_Current_HPI'] * CA_ZIP['Population']
CA_ZIP['Vaccinated_Population_Total'] = CA_ZIP['Rate_Total'] * CA_ZIP['Population']
CA_ZIP['Vaccinated_Population_Total_HPI'] = CA_ZIP['Rate_Total_HPI'] * CA_ZIP['Population']

rate_current = sum(CA_ZIP['Vaccinated_Population_Current'].values) / total_population
rate_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Current'].values) / population1
rate_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Current'].values) / population2
rate_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Current'].values) / population3
rate_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Current'].values) / population4

rate_current_hpi = sum(CA_ZIP['Vaccinated_Population_Current_HPI'].values) / total_population
rate_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Current_HPI'].values) / population1
rate_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Current_HPI'].values) / population2
rate_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Current_HPI'].values) / population3
rate_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Current_HPI'].values) / population4

rate_total = sum(CA_ZIP['Vaccinated_Population_Total'].values) / total_population
rate_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Total'].values) / population1
rate_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Total'].values) / population2
rate_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Total'].values) / population3
rate_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Total'].values) / population4

rate_total_hpi = sum(CA_ZIP['Vaccinated_Population_Total_HPI'].values) / total_population
rate_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI'].values) / population1
rate_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI'].values) / population2
rate_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI'].values) / population3
rate_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI'].values) / population4

# rate = np.array([[rate_current, rate_current1, rate_current2, rate_current3, rate_current4],
#                  [rate_current_hpi, rate_current_hpi1, rate_current_hpi2, rate_current_hpi3, rate_current_hpi4],
#                  [rate_total, rate_total1, rate_total2, rate_total3, rate_total4],
#                  [rate_total_hpi, rate_total_hpi1, rate_total_hpi2, rate_total_hpi3, rate_total_hpi4]
#                  ])

rate = np.array([[rate_current, rate_current1, rate_current2, rate_current3, rate_current4],
                 [rate_total, rate_total1, rate_total2, rate_total3, rate_total4],
                 [rate_current_hpi, rate_current_hpi1, rate_current_hpi2, rate_current_hpi3, rate_current_hpi4],
                 [rate_total_hpi, rate_total_hpi1, rate_total_hpi2, rate_total_hpi3, rate_total_hpi4]
                 ])

# Vaccinated rate and population
rate_table = np.concatenate((np.round(rate,4) * 100, np.round(rate * population_vec / 1000000,2)), axis=1)
print(tabulate(rate_table, tablefmt="latex"))

###########################################################################

### Average distance for each quartile
avg_dist_current = np.nan_to_num(np.sum(np.multiply(C_current, mat_y_current), axis = 1) / np.sum(mat_y_current, axis = 1), posinf=0)
avg_dist_current_hpi = np.nan_to_num(np.sum(np.multiply(C_current, mat_y_current_hpi), axis = 1) / np.sum(mat_y_current_hpi, axis = 1), posinf=0)
avg_dist_total = np.nan_to_num(np.sum(np.multiply(C_total, mat_y_total), axis = 1) / np.sum(mat_y_total, axis = 1), posinf=0)
avg_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(C_total, mat_y_total_hpi), axis = 1) / np.sum(mat_y_total_hpi, axis = 1), posinf=0)

CA_ZIP['Dist_Current'] = avg_dist_current
CA_ZIP['Dist_Current_HPI'] = avg_dist_current_hpi
CA_ZIP['Dist_Total'] = avg_dist_total
CA_ZIP['Dist_Total_HPI'] = avg_dist_total_hpi

CA_ZIP['Allocated_Population_Current'] = np.sum(mat_y_current, axis = 1) * CA_ZIP['Population']
CA_ZIP['Allocated_Population_Current_HPI'] = np.sum(mat_y_current_hpi, axis = 1) * CA_ZIP['Population']
CA_ZIP['Allocated_Population_Total'] = np.sum(mat_y_total, axis = 1) * CA_ZIP['Population']
CA_ZIP['Allocated_Population_Total_HPI'] = np.sum(mat_y_total_hpi, axis = 1) * CA_ZIP['Population']

CA_ZIP['Dist_Current_weighted'] = CA_ZIP['Dist_Current'] * CA_ZIP['Allocated_Population_Current']
CA_ZIP['Dist_Current_HPI_weighted'] = CA_ZIP['Dist_Current_HPI'] * CA_ZIP['Allocated_Population_Current_HPI']
CA_ZIP['Dist_Total_weighted'] = CA_ZIP['Dist_Total'] * CA_ZIP['Allocated_Population_Total']
CA_ZIP['Dist_Total_HPI_weighted'] = CA_ZIP['Dist_Total_HPI'] * CA_ZIP['Allocated_Population_Total_HPI']

avg_dist_current = sum(CA_ZIP['Dist_Current_weighted'].values) / sum(CA_ZIP['Allocated_Population_Current'].values)
avg_dist_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Current_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Allocated_Population_Current'])
avg_dist_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Current_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Allocated_Population_Current'])
avg_dist_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Current_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Allocated_Population_Current'])
avg_dist_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Current_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Allocated_Population_Current'])

avg_dist_current_hpi = sum(CA_ZIP['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP['Allocated_Population_Current_HPI'].values)
avg_dist_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Allocated_Population_Current_HPI'])
avg_dist_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Allocated_Population_Current_HPI'])
avg_dist_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Allocated_Population_Current_HPI'])
avg_dist_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Allocated_Population_Current_HPI'])

avg_dist_total = sum(CA_ZIP['Dist_Total_weighted'].values) / sum(CA_ZIP['Allocated_Population_Total'].values)
avg_dist_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Allocated_Population_Total'])
avg_dist_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Allocated_Population_Total'])
avg_dist_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Allocated_Population_Total'])
avg_dist_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Allocated_Population_Total'])

avg_dist_total_hpi = sum(CA_ZIP['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP['Allocated_Population_Total_HPI'].values)
avg_dist_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Allocated_Population_Total_HPI'])
avg_dist_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Allocated_Population_Total_HPI'])
avg_dist_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Allocated_Population_Total_HPI'])
avg_dist_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Allocated_Population_Total_HPI'])


avg_dist = np.array([[avg_dist_current, avg_dist_current1, avg_dist_current2, avg_dist_current3, avg_dist_current4],
                     [avg_dist_total, avg_dist_total1, avg_dist_total2, avg_dist_total3, avg_dist_total4],
                     [avg_dist_current_hpi, avg_dist_current_hpi1, avg_dist_current_hpi2, avg_dist_current_hpi3, avg_dist_current_hpi4],
                     [avg_dist_total_hpi, avg_dist_total_hpi1, avg_dist_total_hpi2, avg_dist_total_hpi3, avg_dist_total_hpi4]
                     ])

###########################################################################

### Actual distance for each quartile
avg_dist_current = np.nan_to_num(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current)), axis = 1) / np.sum(np.multiply(F_DH_current, mat_y_current), axis = 1), posinf=0)
avg_dist_current_hpi = np.nan_to_num(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current_hpi)), axis = 1) / np.sum(np.multiply(F_DH_current, mat_y_current_hpi), axis = 1), posinf=0)
avg_dist_total = np.nan_to_num(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total)), axis = 1) / np.sum(np.multiply(F_DH_total, mat_y_total), axis = 1), posinf=0)
avg_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1) / np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1), posinf=0)

CA_ZIP['Dist_Current_Actual'] = avg_dist_current
CA_ZIP['Dist_Current_HPI_Actual'] = avg_dist_current_hpi
CA_ZIP['Dist_Total_Actual'] = avg_dist_total
CA_ZIP['Dist_Total_HPI_Actual'] = avg_dist_total_hpi

# either population or distance could be zero
CA_ZIP['Dist_Current_weighted'] = CA_ZIP['Dist_Current_Actual'] * CA_ZIP['Vaccinated_Population_Current']
CA_ZIP['Dist_Current_HPI_weighted'] = CA_ZIP['Dist_Current_HPI_Actual'] * CA_ZIP['Vaccinated_Population_Current_HPI']
CA_ZIP['Dist_Total_weighted'] = CA_ZIP['Dist_Total_Actual'] * CA_ZIP['Vaccinated_Population_Total']
CA_ZIP['Dist_Total_HPI_weighted'] = CA_ZIP['Dist_Total_HPI_Actual'] * CA_ZIP['Vaccinated_Population_Total_HPI']

avg_dist_current = sum(CA_ZIP['Dist_Current_weighted'].values) / sum(CA_ZIP['Vaccinated_Population_Current'].values)
avg_dist_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Current_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Current'])
avg_dist_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Current_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Current'])
avg_dist_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Current_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Current'])
avg_dist_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Current_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Current'])

avg_dist_current_hpi = sum(CA_ZIP['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP['Vaccinated_Population_Current_HPI'].values)
avg_dist_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Current_HPI'])
avg_dist_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Current_HPI'])
avg_dist_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Current_HPI'])
avg_dist_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Current_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Current_HPI'])

avg_dist_total = sum(CA_ZIP['Dist_Total_weighted'].values) / sum(CA_ZIP['Vaccinated_Population_Total'].values)
avg_dist_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Total'])
avg_dist_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Total'])
avg_dist_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Total'])
avg_dist_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Total'])

avg_dist_total_hpi = sum(CA_ZIP['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP['Vaccinated_Population_Total_HPI'].values)
avg_dist_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI'])
avg_dist_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI'])
avg_dist_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI'])
avg_dist_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI'])


# total_dist = np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1) @ CA_ZIP['Population'].values
# total_ppl = np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1) @ CA_ZIP['Population'].values
# avg_dist_current_new = total_dist / total_ppl

# total_dist = (np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1) * CA_ZIP['Population'].values)[CA_ZIP['HPIQuartile'] == 2]
# total_ppl = (np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1) * CA_ZIP['Population'].values)[CA_ZIP['HPIQuartile'] == 2]
# avg_dist_current_new = sum(total_dist) / sum(total_ppl)

avg_dist_actual = np.array([[avg_dist_current, avg_dist_current1, avg_dist_current2, avg_dist_current3, avg_dist_current4],
                            [avg_dist_total, avg_dist_total1, avg_dist_total2, avg_dist_total3, avg_dist_total4],
                            [avg_dist_current_hpi, avg_dist_current_hpi1, avg_dist_current_hpi2, avg_dist_current_hpi3, avg_dist_current_hpi4],
                            [avg_dist_total_hpi, avg_dist_total_hpi1, avg_dist_total_hpi2, avg_dist_total_hpi3, avg_dist_total_hpi4]
                            ])

# dist_table = np.round(np.concatenate((avg_dist, avg_dist_actual), axis=1))
dist_table = np.round(avg_dist_actual)
print(tabulate(dist_table, tablefmt="latex"))

RESULT = np.concatenate((np.round(rate * population_vec / 1000000,2), np.round(avg_dist_actual)), axis=1)
print(tabulate(RESULT, tablefmt="latex"))


###########################################################################

### Within walkable distance ###
walkable_current = np.sum(np.multiply(F_DH_current, np.multiply(C_current_walkable, mat_y_current)), axis = 1)
walkable_current_hpi = np.sum(np.multiply(F_DH_current, np.multiply(C_current_walkable, mat_y_current_hpi)), axis = 1)
walkable_total = np.sum(np.multiply(F_DH_total, np.multiply(C_total_walkable, mat_y_total)), axis = 1)
walkable_total_hpi = np.sum(np.multiply(F_DH_total, np.multiply(C_total_walkable, mat_y_total_hpi)), axis = 1)

CA_ZIP['Walkable_Current'] = walkable_current
CA_ZIP['Walkable_Current_HPI'] = walkable_current_hpi
CA_ZIP['Walkable_Total'] = walkable_total
CA_ZIP['Walkable_Total_HPI'] = walkable_total_hpi

CA_ZIP['Walkable_Population_Current'] = CA_ZIP['Walkable_Current'] * CA_ZIP['Population']
CA_ZIP['Walkable_Population_Current_HPI'] = CA_ZIP['Walkable_Current_HPI'] * CA_ZIP['Population']
CA_ZIP['Walkable_Population_Total'] = CA_ZIP['Walkable_Total'] * CA_ZIP['Population']
CA_ZIP['Walkable_Population_Total_HPI'] = CA_ZIP['Walkable_Total_HPI'] * CA_ZIP['Population']

walkable_current = sum(CA_ZIP['Walkable_Population_Current'].values)
walkable_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Walkable_Population_Current'].values)
walkable_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Walkable_Population_Current'].values)
walkable_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Walkable_Population_Current'].values)
walkable_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Walkable_Population_Current'].values)

walkable_current_hpi = sum(CA_ZIP['Walkable_Population_Current_HPI'].values)
walkable_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Walkable_Population_Current_HPI'].values)
walkable_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Walkable_Population_Current_HPI'].values)
walkable_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Walkable_Population_Current_HPI'].values)
walkable_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Walkable_Population_Current_HPI'].values)

walkable_total = sum(CA_ZIP['Walkable_Population_Total'].values)
walkable_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Walkable_Population_Total'].values)
walkable_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Walkable_Population_Total'].values)
walkable_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Walkable_Population_Total'].values)
walkable_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Walkable_Population_Total'].values)

walkable_total_hpi = sum(CA_ZIP['Walkable_Population_Total_HPI'].values)
walkable_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Walkable_Population_Total_HPI'].values)
walkable_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Walkable_Population_Total_HPI'].values)
walkable_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Walkable_Population_Total_HPI'].values)
walkable_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Walkable_Population_Total_HPI'].values)

### Assigned instead of vaccinated
assigned_current = np.sum(np.multiply(C_current_walkable, mat_y_current), axis = 1)
assigned_current_hpi = np.sum(np.multiply(C_current_walkable, mat_y_current_hpi), axis = 1)
assigned_total = np.sum(np.multiply(C_total_walkable, mat_y_total), axis = 1)
assigned_total_hpi = np.sum(np.multiply(C_total_walkable, mat_y_total_hpi), axis = 1)

CA_ZIP['Assigned_Current'] = assigned_current
CA_ZIP['Assigned_Current_HPI'] = assigned_current_hpi
CA_ZIP['Assigned_Total'] = assigned_total
CA_ZIP['Assigned_Total_HPI'] = assigned_total_hpi

CA_ZIP['Assigned_Population_Current'] = CA_ZIP['Assigned_Current'] * CA_ZIP['Population']
CA_ZIP['Assigned_Population_Current_HPI'] = CA_ZIP['Assigned_Current_HPI'] * CA_ZIP['Population']
CA_ZIP['Assigned_Population_Total'] = CA_ZIP['Assigned_Total'] * CA_ZIP['Population']
CA_ZIP['Assigned_Population_Total_HPI'] = CA_ZIP['Assigned_Total_HPI'] * CA_ZIP['Population']

assigned_current = sum(CA_ZIP['Assigned_Population_Current'].values)
assigned_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Assigned_Population_Current'].values)
assigned_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Assigned_Population_Current'].values)
assigned_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Assigned_Population_Current'].values)
assigned_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Assigned_Population_Current'].values)

assigned_current_hpi = sum(CA_ZIP['Assigned_Population_Current_HPI'].values)
assigned_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Assigned_Population_Current_HPI'].values)
assigned_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Assigned_Population_Current_HPI'].values)
assigned_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Assigned_Population_Current_HPI'].values)
assigned_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Assigned_Population_Current_HPI'].values)

assigned_total = sum(CA_ZIP['Assigned_Population_Total'].values)
assigned_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Assigned_Population_Total'].values)
assigned_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Assigned_Population_Total'].values)
assigned_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Assigned_Population_Total'].values)
assigned_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Assigned_Population_Total'].values)

assigned_total_hpi = sum(CA_ZIP['Assigned_Population_Total_HPI'].values)
assigned_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Assigned_Population_Total_HPI'].values)
assigned_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Assigned_Population_Total_HPI'].values)
assigned_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Assigned_Population_Total_HPI'].values)
assigned_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Assigned_Population_Total_HPI'].values)

walkable = np.array([[walkable_current, walkable_current1, walkable_current2, walkable_current3, walkable_current4,
                      assigned_current, assigned_current1, assigned_current2, assigned_current3, assigned_current4],
                     [walkable_current_hpi, walkable_current_hpi1, walkable_current_hpi2, walkable_current_hpi3, walkable_current_hpi4,
                      assigned_current_hpi, assigned_current_hpi1, assigned_current_hpi2, assigned_current_hpi3, assigned_current_hpi4],
                     [walkable_total, walkable_total1, walkable_total2, walkable_total3, walkable_total4,
                      assigned_total, assigned_total1, assigned_total2, assigned_total3, assigned_total4],                    
                     [walkable_total_hpi, walkable_total_hpi1, walkable_total_hpi2, walkable_total_hpi3, walkable_total_hpi4,
                      assigned_total_hpi, assigned_total_hpi1, assigned_total_hpi2, assigned_total_hpi3, assigned_total_hpi4]
                     ])

walkable_table = np.round(walkable / 1000000,2)
print(tabulate(walkable_table, tablefmt="latex"))


###########################################################################

### Desert ###
desert_current = np.sum(np.multiply(F_DH_current, np.multiply(C_current_desert, mat_y_current)), axis = 1)
desert_current_hpi = np.sum(np.multiply(F_DH_current, np.multiply(C_current_desert, mat_y_current_hpi)), axis = 1)
desert_total = np.sum(np.multiply(F_DH_total, np.multiply(C_total_desert, mat_y_total)), axis = 1)
desert_total_hpi = np.sum(np.multiply(F_DH_total, np.multiply(C_total_desert, mat_y_total_hpi)), axis = 1)

CA_ZIP['Desert_Current'] = desert_current
CA_ZIP['Desert_Current_HPI'] = desert_current_hpi
CA_ZIP['Desert_Total'] = desert_total
CA_ZIP['Desert_Total_HPI'] = desert_total_hpi

CA_ZIP['Desert_Population_Current'] = CA_ZIP['Desert_Current'] * CA_ZIP['Population']
CA_ZIP['Desert_Population_Current_HPI'] = CA_ZIP['Desert_Current_HPI'] * CA_ZIP['Population']
CA_ZIP['Desert_Population_Total'] = CA_ZIP['Desert_Total'] * CA_ZIP['Population']
CA_ZIP['Desert_Population_Total_HPI'] = CA_ZIP['Desert_Total_HPI'] * CA_ZIP['Population']

desert_current = sum(CA_ZIP['Desert_Population_Current'].values)
desert_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Desert_Population_Current'].values)
desert_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Desert_Population_Current'].values)
desert_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Desert_Population_Current'].values)
desert_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Desert_Population_Current'].values)

desert_current_hpi = sum(CA_ZIP['Desert_Population_Current_HPI'].values)
desert_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Desert_Population_Current_HPI'].values)
desert_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Desert_Population_Current_HPI'].values)
desert_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Desert_Population_Current_HPI'].values)
desert_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Desert_Population_Current_HPI'].values)

desert_total = sum(CA_ZIP['Desert_Population_Total'].values)
desert_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Desert_Population_Total'].values)
desert_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Desert_Population_Total'].values)
desert_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Desert_Population_Total'].values)
desert_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Desert_Population_Total'].values)

desert_total_hpi = sum(CA_ZIP['Desert_Population_Total_HPI'].values)
desert_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Desert_Population_Total_HPI'].values)
desert_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Desert_Population_Total_HPI'].values)
desert_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Desert_Population_Total_HPI'].values)
desert_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Desert_Population_Total_HPI'].values)

### Assigned instead of vaccinated
assigned_current = np.sum(np.multiply(C_current_desert, mat_y_current), axis = 1)
assigned_current_hpi = np.sum(np.multiply(C_current_desert, mat_y_current_hpi), axis = 1)
assigned_total = np.sum(np.multiply(C_total_desert, mat_y_total), axis = 1)
assigned_total_hpi = np.sum(np.multiply(C_total_desert, mat_y_total_hpi), axis = 1)

CA_ZIP['Assigned_Current'] = assigned_current
CA_ZIP['Assigned_Current_HPI'] = assigned_current_hpi
CA_ZIP['Assigned_Total'] = assigned_total
CA_ZIP['Assigned_Total_HPI'] = assigned_total_hpi

CA_ZIP['Assigned_Population_Current'] = CA_ZIP['Assigned_Current'] * CA_ZIP['Population']
CA_ZIP['Assigned_Population_Current_HPI'] = CA_ZIP['Assigned_Current_HPI'] * CA_ZIP['Population']
CA_ZIP['Assigned_Population_Total'] = CA_ZIP['Assigned_Total'] * CA_ZIP['Population']
CA_ZIP['Assigned_Population_Total_HPI'] = CA_ZIP['Assigned_Total_HPI'] * CA_ZIP['Population']

assigned_current = sum(CA_ZIP['Assigned_Population_Current'].values)
assigned_current1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Assigned_Population_Current'].values)
assigned_current2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Assigned_Population_Current'].values)
assigned_current3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Assigned_Population_Current'].values)
assigned_current4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Assigned_Population_Current'].values)

assigned_current_hpi = sum(CA_ZIP['Assigned_Population_Current_HPI'].values)
assigned_current_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Assigned_Population_Current_HPI'].values)
assigned_current_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Assigned_Population_Current_HPI'].values)
assigned_current_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Assigned_Population_Current_HPI'].values)
assigned_current_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Assigned_Population_Current_HPI'].values)

assigned_total = sum(CA_ZIP['Assigned_Population_Total'].values)
assigned_total1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Assigned_Population_Total'].values)
assigned_total2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Assigned_Population_Total'].values)
assigned_total3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Assigned_Population_Total'].values)
assigned_total4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Assigned_Population_Total'].values)

assigned_total_hpi = sum(CA_ZIP['Assigned_Population_Total_HPI'].values)
assigned_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Assigned_Population_Total_HPI'].values)
assigned_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Assigned_Population_Total_HPI'].values)
assigned_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Assigned_Population_Total_HPI'].values)
assigned_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Assigned_Population_Total_HPI'].values)

desert = np.array([[desert_current, desert_current1, desert_current2, desert_current3, desert_current4,
                      assigned_current, assigned_current1, assigned_current2, assigned_current3, assigned_current4],
                     [desert_current_hpi, desert_current_hpi1, desert_current_hpi2, desert_current_hpi3, desert_current_hpi4,
                      assigned_current_hpi, assigned_current_hpi1, assigned_current_hpi2, assigned_current_hpi3, assigned_current_hpi4],
                     [desert_total, desert_total1, desert_total2, desert_total3, desert_total4,
                      assigned_total, assigned_total1, assigned_total2, assigned_total3, assigned_total4],                    
                     [desert_total_hpi, desert_total_hpi1, desert_total_hpi2, desert_total_hpi3, desert_total_hpi4,
                      assigned_total_hpi, assigned_total_hpi1, assigned_total_hpi2, assigned_total_hpi3, assigned_total_hpi4]
                     ])

desert_table = np.round(desert / 1000000,2)
print(tabulate(desert_table, tablefmt="latex"))

CA_ZIP.to_csv(path + 'CA_desert.csv', index = False)

