#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 5, 2022
"""

import os
import pandas as pd
import numpy as np

os.chdir('/Users/jingyuanhu/Desktop/Research/COVID_project/Submission MS/Code')

###########################################################################

### Zip code ###

CA_ZIP = pd.read_csv('../Data/CaliforniaZipHPI.csv', delimiter = ",") 
Population = CA_ZIP['Population'].values
total_population = sum(Population)
Quartile = CA_ZIP['HPIQuartile'].values.astype(int)

population1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Population'].values)
population2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Population'].values)
population3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Population'].values)
population4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Population'].values)
population_vec = [total_population, population1, population2, population3, population4]

C_current = np.genfromtxt('../Data/dist_matrix_CA_current.csv', delimiter = ",", dtype = float)
C_current = C_current.astype(int)
C_current = C_current.T
num_zips, num_current_stores = np.shape(C_current)
closest_dist_current = np.min(C_current, axis = 1)
CA_ZIP['Closest_Dist_Current'] = closest_dist_current

C_dollar = np.genfromtxt('../Data/dist_matrix_CA_dollar.csv', delimiter = ",", dtype = float)
C_dollar = C_dollar.astype(int)
C_dollar = C_dollar.T
num_zips, num_dollar_stores = np.shape(C_dollar)

C_total = np.concatenate((C_current, C_dollar), axis = 1)
num_total_stores = num_current_stores + num_dollar_stores
closest_dist_total = np.min(C_total, axis = 1)
CA_ZIP['Closest_Dist_Total'] = closest_dist_total

###########################################################################

### Census Tract ###

# Population = np.genfromtxt('../Data/population_tract.csv', delimiter = ",", dtype = int)
# total_population = sum(Population)
# Quartile = np.genfromtxt('../Data/quartile_tract.csv', delimiter = ",", dtype = int)
# CA_ZIP = pd.DataFrame(data = {'Population': Population, 'HPIQuartile': Quartile})

# population1 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 1]['Population'].values)
# population2 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 2]['Population'].values)
# population3 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 3]['Population'].values)
# population4 = sum(CA_ZIP[CA_ZIP['HPIQuartile'] == 4]['Population'].values)
# population_vec = [total_population, population1, population2, population3, population4]

# C_current = np.genfromtxt('../Data/dist_matrix_CA_current_tract.csv', delimiter = ",", dtype = float)
# C_current = C_current.astype(int)
# C_current = C_current.T
# num_zips, num_current_stores = np.shape(C_current)
   
# C_dollar = np.genfromtxt('../Data/dist_matrix_CA_dollar_tract.csv', delimiter = ",", dtype = float)
# C_dollar = C_dollar.astype(int)
# C_dollar = C_dollar.T
# num_zips, num_dollar_stores = np.shape(C_dollar)

# C_total = np.concatenate((C_current, C_dollar), axis = 1)
# num_total_stores = num_current_stores + num_dollar_stores

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
# path = '../Result/Zip_0.84capacity_N5/'
path = '../Result/Zip_0.84capacity_N10/'
# path = '../Result/Zip_0.84capacity_N20/'
# path = '../Result/Zip_0.84capacity_N50/'
# path = '../Result/Zip_0.84capacity_N100/'
# path = '../Result/Tract_0.84capacity_N20/'
# path = '../Result/Tract_0.84capacity_N50/'

y_current = np.genfromtxt(path + 'Dist/y_current.csv', delimiter = ",", dtype = float)
y_current_hpi = np.genfromtxt(path + 'HPI_Dist/y_current.csv', delimiter = ",", dtype = float)
y_total = np.genfromtxt(path + 'Dist/y_total.csv', delimiter = ",", dtype = float)
y_total_hpi = np.genfromtxt(path + 'HPI_Dist/y_total.csv', delimiter = ",", dtype = float)

mat_y_current = np.reshape(y_current, (num_zips, num_current_stores))
mat_y_current_hpi = np.reshape(y_current_hpi, (num_zips, num_current_stores))
mat_y_total = np.reshape(y_total, (num_zips, num_total_stores))
mat_y_total_hpi = np.reshape(y_total_hpi, (num_zips, num_total_stores))

###########################################################################

### Rate for each quartile
rate_current = np.sum(np.multiply(F_DH_current, mat_y_current), axis = 1)
rate_current_hpi = np.sum(np.multiply(F_DH_current, mat_y_current_hpi), axis = 1)
rate_total = np.sum(np.multiply(F_DH_total, mat_y_total), axis = 1)
rate_total_hpi = np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1)

CA_ZIP['Rate_Current'] = np.round(rate_current,4)
CA_ZIP['Rate_Current_HPI'] = np.round(rate_current_hpi,4)
CA_ZIP['Rate_Total'] = np.round(rate_total,4)
CA_ZIP['Rate_Total_HPI'] = np.round(rate_total_hpi,4)


### Average distance for each quartile
avg_dist_current = np.round(np.sum(np.multiply(C_current, mat_y_current), axis = 1),1)
avg_dist_current_hpi = np.round(np.sum(np.multiply(C_current, mat_y_current_hpi), axis = 1),1)
avg_dist_total = np.round(np.sum(np.multiply(C_total, mat_y_total), axis = 1),1)
avg_dist_total_hpi = np.round(np.sum(np.multiply(C_total, mat_y_total_hpi), axis = 1),1)

CA_ZIP['Dist_Current'] = np.round(avg_dist_current)
CA_ZIP['Dist_Current_HPI'] = np.round(avg_dist_current_hpi)
CA_ZIP['Dist_Total'] = np.round(avg_dist_total)
CA_ZIP['Dist_Total_HPI'] = np.round(avg_dist_total_hpi)


### Actual distance for each quartile
avg_dist_current_actual = np.round(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current)), axis = 1),1)
avg_dist_current_hpi_actual = np.round(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current_hpi)), axis = 1),1)
avg_dist_total_actual = np.round(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total)), axis = 1),1)
avg_dist_total_hpi_actual = np.round(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1),1)

CA_ZIP['Dist_Current_Actual'] = np.round(avg_dist_current_actual)
CA_ZIP['Dist_Current_HPI_Actual'] = np.round(avg_dist_current_hpi_actual)
CA_ZIP['Dist_Total_Actual'] = np.round(avg_dist_total_actual)
CA_ZIP['Dist_Total_HPI_Actual'] = np.round(avg_dist_total_hpi_actual)

###########################################################################

### Number of current stores used
current_stores_current = np.sum(np.ceil(mat_y_current[:, 0:num_current_stores]), axis = 1)
current_stores_current_hpi = np.sum(np.ceil(mat_y_current_hpi[:, 0:num_current_stores]), axis = 1)
current_stores_total = np.sum(np.ceil(mat_y_total[:, 0:num_current_stores]), axis = 1)
current_stores_total_hpi = np.sum(np.ceil(mat_y_total_hpi[:, 0:num_current_stores]), axis = 1)

CA_ZIP['Pharmacy_Current'] = current_stores_current
CA_ZIP['Pharmacy_Current_HPI'] = current_stores_current_hpi


### Number of dollar stores used
dollar_stores_current = np.zeros(num_zips, dtype = int)
dollar_stores_current_hpi = np.zeros(num_zips, dtype = int)
dollar_stores_total = np.sum(np.ceil(mat_y_total[:, num_current_stores:num_total_stores]), axis = 1)
dollar_stores_total_hpi = np.sum(np.ceil(mat_y_total_hpi[:, num_current_stores:num_total_stores]), axis = 1)

CA_ZIP['Pharmacy_Total'] = current_stores_total
CA_ZIP['Dollar_Total'] = dollar_stores_total
CA_ZIP['Pharmacy_Total_HPI'] = current_stores_total_hpi
CA_ZIP['Dollar_Total_HPI'] = dollar_stores_total_hpi


### Actual demand covered by current stores & dollar stores
### Note: under current, this is equal to vaccination rate
CA_ZIP['Demand_by_Pharmacy'] = np.sum(mat_y_total[:,0:num_current_stores], axis = 1)
CA_ZIP['Demand_by_Dollar'] = np.sum(mat_y_total[:,num_current_stores:num_total_stores], axis = 1)
CA_ZIP['Demand_by_Pharmacy(HPI)'] = np.sum(mat_y_total_hpi[:,0:num_current_stores], axis = 1)
CA_ZIP['Demand_by_Dollar(HPI)'] = np.sum(mat_y_total_hpi[:,num_current_stores:num_total_stores], axis = 1)

CA_ZIP['Demand_by_Pharmacy_Actual'] = np.sum(np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores], axis = 1)
CA_ZIP['Demand_by_Dollar_Actual'] = np.sum(np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores], axis = 1)
CA_ZIP['Demand_by_Pharmacy(HPI)_Actual'] = np.sum(np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores], axis = 1)
CA_ZIP['Demand_by_Dollar(HPI)_Actual'] = np.sum(np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores], axis = 1)

###########################################################################

### Closest distance to store
CA_ZIP['Closest_Current'] = np.round(C_current.min(axis=1))
CA_ZIP['Closest_Dollar'] = np.round(C_dollar.min(axis=1))

###########################################################################

CA_ZIP.to_csv(path + 'CA.csv', index = False)
