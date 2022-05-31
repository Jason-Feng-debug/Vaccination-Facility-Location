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
TRACT_RAW = pd.read_csv('../Data/Tract_CA.csv', delimiter = ",")
Population = np.genfromtxt('../Data/population_tract.csv', delimiter = ",", dtype = int)
total_population = sum(Population)
Quartile = np.genfromtxt('../Data/quartile_tract.csv', delimiter = ",", dtype = int)
CA_TRACT = pd.DataFrame(data = {'FIPS': TRACT_RAW['FIPS'],
                                'County': TRACT_RAW['COUNTY'],
                                'Tract': TRACT_RAW['TRACT'],
                                'Latitude': TRACT_RAW['LATITUDE'],
                                'Longitude': TRACT_RAW['LONGITUDE'],
                                'Population': Population, 'HPIQuartile': Quartile})

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

# Import solution
# path = '../Result/Zip_0.84capacity_N5/'
# path = '../Result/Zip_0.84capacity_N10/'
# path = '../Result/Zip_0.84capacity_N20/'
# path = '../Result/Zip_0.84capacity_N50/'
# path = '../Result/Zip_0.84capacity_N100/'
# path = '../Result/Tract_0.7capacity_N10/'
path = '../Result/Tract_0.84capacity_N10/'
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

### Stores ###
Current = pd.read_csv(path + 'CurrentStores_Tract_N10.csv', delimiter = ",")
Dollar = pd.read_csv(path + 'DollarStores_Tract_N10.csv', delimiter = ",")

###########################################################################

### Rate for each quartile
rate_current = np.sum(np.multiply(F_DH_current, mat_y_current), axis = 1)
rate_current_hpi = np.sum(np.multiply(F_DH_current, mat_y_current_hpi), axis = 1)
rate_total = np.sum(np.multiply(F_DH_total, mat_y_total), axis = 1)
rate_total_hpi = np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1)

# CA_TRACT['Rate_Current_Dist'] = np.round(rate_current,4)
# CA_TRACT['Rate_Current_DistHPI'] = np.round(rate_current_hpi,4)
# CA_TRACT['Rate_Total_Dist'] = np.round(rate_total,4)
# CA_TRACT['Rate_Total_DistHPI'] = np.round(rate_total_hpi,4)

CA_TRACT['Rate_Current_Dist'] = rate_current
CA_TRACT['Rate_Current_DistHPI'] = rate_current_hpi
CA_TRACT['Rate_Total_Dist'] = rate_total
CA_TRACT['Rate_Total_DistHPI'] = rate_total_hpi


### Average distance for each quartile
avg_dist_current = np.nan_to_num(np.sum(np.multiply(C_current, mat_y_current), axis = 1) / np.sum(mat_y_current, axis = 1), posinf=0)
avg_dist_current_hpi = np.nan_to_num(np.sum(np.multiply(C_current, mat_y_current_hpi), axis = 1) / np.sum(mat_y_current_hpi, axis = 1), posinf=0)
avg_dist_total = np.nan_to_num(np.sum(np.multiply(C_total, mat_y_total), axis = 1) / np.sum(mat_y_total, axis = 1), posinf=0)
avg_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(C_total, mat_y_total_hpi), axis = 1) / np.sum(mat_y_total_hpi, axis = 1), posinf=0)

CA_TRACT['Dist_Current_Dist'] = np.round(avg_dist_current)
CA_TRACT['Dist_Current_DistHPI'] = np.round(avg_dist_current_hpi)
CA_TRACT['Dist_Total_Dist'] = np.round(avg_dist_total)
CA_TRACT['Dist_Total_DistHPI'] = np.round(avg_dist_total_hpi)


### Actual distance for each quartile
avg_dist_current_actual = np.nan_to_num(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current)), axis = 1) / np.sum(np.multiply(F_DH_current, mat_y_current), axis = 1), posinf=0)
avg_dist_current_hpi_actual = np.nan_to_num(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current_hpi)), axis = 1) / np.sum(np.multiply(F_DH_current, mat_y_current_hpi), axis = 1), posinf=0)
avg_dist_total_actual = np.nan_to_num(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total)), axis = 1) / np.sum(np.multiply(F_DH_total, mat_y_total), axis = 1), posinf=0)
avg_dist_total_hpi_actual = np.nan_to_num(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1) / np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1), posinf=0)

CA_TRACT['ActualDist_Current_Dist'] = np.round(avg_dist_current_actual)
CA_TRACT['ActualDist_Current_DistHPI'] = np.round(avg_dist_current_hpi_actual)
CA_TRACT['ActualDist_Total_Dist'] = np.round(avg_dist_total_actual)
CA_TRACT['ActualDist_Total_DistHPI'] = np.round(avg_dist_total_hpi_actual)

###########################################################################

### Number of current stores used
current_stores_current = np.sum(np.ceil(mat_y_current[:, 0:num_current_stores]), axis = 1)
current_stores_current_hpi = np.sum(np.ceil(mat_y_current_hpi[:, 0:num_current_stores]), axis = 1)
current_stores_total = np.sum(np.ceil(mat_y_total[:, 0:num_current_stores]), axis = 1)
current_stores_total_hpi = np.sum(np.ceil(mat_y_total_hpi[:, 0:num_current_stores]), axis = 1)

CA_TRACT['Num_Pharmacy_Current_Dist'] = current_stores_current
CA_TRACT['Num_Pharmacy_Current_DistHPI'] = current_stores_current_hpi


### Number of dollar stores used
dollar_stores_total = np.sum(np.ceil(mat_y_total[:, num_current_stores:num_total_stores]), axis = 1)
dollar_stores_total_hpi = np.sum(np.ceil(mat_y_total_hpi[:, num_current_stores:num_total_stores]), axis = 1)

CA_TRACT['Num_Pharmacy_Total_Dist'] = current_stores_total
CA_TRACT['Num_Dollar_Total_Dist'] = dollar_stores_total
CA_TRACT['Num_Pharmacy_Total_DistHPI'] = current_stores_total_hpi
CA_TRACT['Num_Dollar_Total_DistHPI'] = dollar_stores_total_hpi


### Actual demand covered by current stores & dollar stores
### Note: under current, this is equal to vaccination rate
# CA_TRACT['Demand_by_Pharmacy'] = np.sum(mat_y_total[:,0:num_current_stores], axis = 1)
# CA_TRACT['Demand_by_Dollar'] = np.sum(mat_y_total[:,num_current_stores:num_total_stores], axis = 1)
# CA_TRACT['Demand_by_Pharmacy(HPI)'] = np.sum(mat_y_total_hpi[:,0:num_current_stores], axis = 1)
# CA_TRACT['Demand_by_Dollar(HPI)'] = np.sum(mat_y_total_hpi[:,num_current_stores:num_total_stores], axis = 1)

CA_TRACT['Demand_by_Pharmacy_Total_Dist'] = np.sum(np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores], axis = 1)
CA_TRACT['Demand_by_Dollar_Total_Dist'] = np.sum(np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores], axis = 1)
CA_TRACT['Demand_by_Pharmacy_Total_DistHPI'] = np.sum(np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores], axis = 1)
CA_TRACT['Demand_by_Dollar_Total_DistHPI'] = np.sum(np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores], axis = 1)

###########################################################################

### Demand covered by current & dollar stores, by HPI

# Current stores
CA_TRACT['Demand_by_Pharmacy1_Current_Dist'] = np.sum((np.multiply(F_DH_current, mat_y_current).T)[Current['HPIQuartile'] == 1], axis = 0)
CA_TRACT['Demand_by_Pharmacy1_Current_DistHPI'] = np.sum((np.multiply(F_DH_current, mat_y_current_hpi).T)[Current['HPIQuartile'] == 1], axis = 0)

CA_TRACT['Demand_by_Pharmacy2_Current_Dist'] = np.sum((np.multiply(F_DH_current, mat_y_current).T)[Current['HPIQuartile'] == 2], axis = 0)
CA_TRACT['Demand_by_Pharmacy2_Current_DistHPI'] = np.sum((np.multiply(F_DH_current, mat_y_current_hpi).T)[Current['HPIQuartile'] == 2], axis = 0)

CA_TRACT['Demand_by_Pharmacy3_Current_Dist'] = np.sum((np.multiply(F_DH_current, mat_y_current).T)[Current['HPIQuartile'] == 3], axis = 0)
CA_TRACT['Demand_by_Pharmacy3_Current_DistHPI'] = np.sum((np.multiply(F_DH_current, mat_y_current_hpi).T)[Current['HPIQuartile'] == 3], axis = 0)

CA_TRACT['Demand_by_Pharmacy4_Current_Dist'] = np.sum((np.multiply(F_DH_current, mat_y_current).T)[Current['HPIQuartile'] == 4], axis = 0)
CA_TRACT['Demand_by_Pharmacy4_Current_DistHPI'] = np.sum((np.multiply(F_DH_current, mat_y_current_hpi).T)[Current['HPIQuartile'] == 4], axis = 0)


# Total stores
CA_TRACT['Demand_by_Pharmacy1_Total_Dist'] = np.sum((np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores].T)[Current['HPIQuartile'] == 1], axis = 0)
CA_TRACT['Demand_by_Dollar1_Total_Dist'] = np.sum((np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores].T)[Dollar['HPIQuartile'] == 1], axis = 0)
CA_TRACT['Demand_by_Pharmacy1_Total_DistHPI'] = np.sum((np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores].T)[Current['HPIQuartile'] == 1], axis = 0)
CA_TRACT['Demand_by_Dollar1_Total_DistHPI'] = np.sum((np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores].T)[Dollar['HPIQuartile'] == 1], axis = 0)

CA_TRACT['Demand_by_Pharmacy2_Total_Dist'] = np.sum((np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores].T)[Current['HPIQuartile'] == 2], axis = 0)
CA_TRACT['Demand_by_Dollar2_Total_Dist'] = np.sum((np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores].T)[Dollar['HPIQuartile'] == 2], axis = 0)
CA_TRACT['Demand_by_Pharmacy2_Total_DistHPI'] = np.sum((np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores].T)[Current['HPIQuartile'] == 2], axis = 0)
CA_TRACT['Demand_by_Dollar2_Total_DistHPI'] = np.sum((np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores].T)[Dollar['HPIQuartile'] == 2], axis = 0)

CA_TRACT['Demand_by_Pharmacy3_Total_Dist'] = np.sum((np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores].T)[Current['HPIQuartile'] == 3], axis = 0)
CA_TRACT['Demand_by_Dollar3_Total_Dist'] = np.sum((np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores].T)[Dollar['HPIQuartile'] == 3], axis = 0)
CA_TRACT['Demand_by_Pharmacy3_Total_DistHPI'] = np.sum((np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores].T)[Current['HPIQuartile'] == 3], axis = 0)
CA_TRACT['Demand_by_Dollar3_Total_DistHPI'] = np.sum((np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores].T)[Dollar['HPIQuartile'] == 3], axis = 0)

CA_TRACT['Demand_by_Pharmacy4_Total_Dist'] = np.sum((np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores].T)[Current['HPIQuartile'] == 4], axis = 0)
CA_TRACT['Demand_by_Dollar4_Total_Dist'] = np.sum((np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores].T)[Dollar['HPIQuartile'] == 4], axis = 0)
CA_TRACT['Demand_by_Pharmacy4_Total_DistHPI'] = np.sum((np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores].T)[Current['HPIQuartile'] == 4], axis = 0)
CA_TRACT['Demand_by_Dollar4_Total_DistHPI'] = np.sum((np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores].T)[Dollar['HPIQuartile'] == 4], axis = 0)

###########################################################################

### Utilization rate of stores nearby
CURRENT = pd.read_csv(path + 'CurrentStores_Tract_N10.csv', delimiter = ",")
DOLLAR = pd.read_csv(path + 'DollarStores_Tract_N10.csv', delimiter = ",")

# Note: some utilization rate exceeds 1 for some solution under F_D, as the rate is computed using F_DH

# Current stores
CA_TRACT['Utilization_Pharmacy_Nearby_Current_Dist'] = np.multiply(F_DH_current, mat_y_current) @ CURRENT['Utilization_Current_Dist'].values
CA_TRACT['Utilization_Pharmacy_Nearby_Current_DistHPI'] = np.multiply(F_DH_current, mat_y_current_hpi) @ CURRENT['Utilization_Current_DistHPI'].values
CA_TRACT['Utilization_Scaled_Pharmacy_Nearby_Current_Dist'] = np.multiply(F_DH_current, mat_y_current) @ CURRENT['Utilization_Current_Dist'].values / np.sum(np.multiply(F_DH_current, mat_y_current), axis=1)
CA_TRACT['Utilization_Scaled_Pharmacy_Nearby_Current_DistHPI'] = np.multiply(F_DH_current, mat_y_current_hpi) @ CURRENT['Utilization_Current_DistHPI'].values / np.sum(np.multiply(F_DH_current, mat_y_current_hpi), axis=1)

# Total stores
# 0/0 encountered, set as 0
CA_TRACT['Utilization_Pharmacy_Nearby_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores] @ CURRENT['Utilization_Total_Dist'].values
CA_TRACT['Utilization_Dollar_Nearby_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores] @ DOLLAR['Utilization_Total_Dist'].values
CA_TRACT['Utilization_Scaled_Pharmacy_Nearby_Total_Dist'] = np.nan_to_num(np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores] @ CURRENT['Utilization_Total_Dist'].values / np.sum(np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores], axis=1))
CA_TRACT['Utilization_Scaled_Dollar_Nearby_Total_Dist'] = np.nan_to_num(np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores] @ DOLLAR['Utilization_Total_Dist'].values / np.sum(np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores], axis=1))

CA_TRACT['Utilization_Pharmacy_Nearby_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores] @ CURRENT['Utilization_Total_DistHPI'].values
CA_TRACT['Utilization_Dollar_Nearby_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores] @ DOLLAR['Utilization_Total_DistHPI'].values
CA_TRACT['Utilization_Scaled_Pharmacy_Nearby_Total_DistHPI'] = np.nan_to_num(np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores] @ CURRENT['Utilization_Total_DistHPI'].values / np.sum(np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores], axis=1))
CA_TRACT['Utilization_Scaled_Dollar_Nearby_Total_DistHPI'] = np.nan_to_num(np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores] @ DOLLAR['Utilization_Total_DistHPI'].values / np.sum(np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores], axis=1))

###########################################################################

### Closest distance to store
CA_TRACT['Closest_Current'] = np.round(C_current.min(axis=1))
CA_TRACT['Closest_Dollar'] = np.round(C_dollar.min(axis=1))

###########################################################################

### Export
CA_TRACT.to_csv(path + 'CA.csv', index = False)
