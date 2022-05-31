#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 19, 2022
@Author: Jingyuan Hu
"""

import os
import pandas as pd
import numpy as np
from tabulate import tabulate

os.chdir('/Users/jingyuanhu/Desktop/Research/COVID_project/Submission MS/Code')

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
path = '../Result/Tract/50/'
y_total_hpi = np.genfromtxt(path + 'HPI_Dist/y_total.csv', delimiter = ",", dtype = float)
mat_y_total_hpi = np.reshape(y_total_hpi, (num_zips, num_total_stores))

###########################################################################

### Vaccination rate for each quartile
rate_total_hpi = np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1)

CA_ZIP['Rate_Total_HPI'] = rate_total_hpi
CA_ZIP['Vaccinated_Population_Total_HPI'] = CA_ZIP['Rate_Total_HPI'] * CA_ZIP['Population']

rate_total_hpi = sum(CA_ZIP['Vaccinated_Population_Total_HPI'].values) / total_population
rate_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI'].values) / population1
rate_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI'].values) / population2
rate_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI'].values) / population3
rate_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI'].values) / population4

rate = np.array([[rate_total_hpi, rate_total_hpi1, rate_total_hpi2, rate_total_hpi3, rate_total_hpi4]])

# Vaccinated rate and population
rate_table = np.concatenate((np.round(rate,4) * 100, np.round(rate * population_vec / 1000000,2)), axis=1)
print(tabulate(rate_table, tablefmt="latex"))
 
###########################################################################

### Average distance for each quartile
avg_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(C_total, mat_y_total_hpi), axis = 1) / np.sum(mat_y_total_hpi, axis = 1), posinf=0)

CA_ZIP['Dist_Total_HPI'] = avg_dist_total_hpi
CA_ZIP['Allocated_Population_Total_HPI'] = np.sum(mat_y_total_hpi, axis = 1) * CA_ZIP['Population']
CA_ZIP['Dist_Total_HPI_weighted'] = CA_ZIP['Dist_Total_HPI'] * CA_ZIP['Allocated_Population_Total_HPI']

avg_dist_total_hpi = sum(CA_ZIP['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP['Allocated_Population_Total_HPI'].values)
avg_dist_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Allocated_Population_Total_HPI'])
avg_dist_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Allocated_Population_Total_HPI'])
avg_dist_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Allocated_Population_Total_HPI'])
avg_dist_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Allocated_Population_Total_HPI'])

avg_dist = np.array([[avg_dist_total_hpi, avg_dist_total_hpi1, avg_dist_total_hpi2, avg_dist_total_hpi3, avg_dist_total_hpi4]])

###########################################################################

### Actual distance for each quartile
avg_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1) / np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1), posinf=0)

CA_ZIP['Dist_Total_HPI_Actual'] = avg_dist_total_hpi
CA_ZIP['Dist_Total_HPI_weighted'] = CA_ZIP['Dist_Total_HPI_Actual'] * CA_ZIP['Vaccinated_Population_Total_HPI']

avg_dist_total_hpi = sum(CA_ZIP['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP['Vaccinated_Population_Total_HPI'].values)
avg_dist_total_hpi1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI'])
avg_dist_total_hpi2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI'])
avg_dist_total_hpi3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI'])
avg_dist_total_hpi4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI'])

avg_dist_actual = np.array([[avg_dist_total_hpi, avg_dist_total_hpi1, avg_dist_total_hpi2, avg_dist_total_hpi3, avg_dist_total_hpi4]])

print(tabulate(np.round(avg_dist_actual), tablefmt="latex"))

# dist_table = np.round(np.concatenate((avg_dist, avg_dist_actual), axis=1))
# print(tabulate(dist_table, tablefmt="latex"))
