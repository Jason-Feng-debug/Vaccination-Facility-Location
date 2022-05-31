#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 11, 2022
@Author: Jingyuan Hu

Create a store table with summary statistics from optimization

"""
import os
import pandas as pd
import numpy as np
from tabulate import tabulate

os.chdir('/Users/jingyuanhu/Desktop/Research/COVID project/Submission MS/Code')

###########################################################################

### Stores ###
Current = pd.read_csv('../Data/Current_stores_CA.csv', delimiter = ",")
Dollar = pd.read_csv('../Data/Dollar_stores_CA.csv', delimiter = ",")

### Census Tract ###
Population = np.genfromtxt('../Data/population_tract.csv', delimiter = ",", dtype = int)
total_population = sum(Population)
Quartile = np.genfromtxt('../Data/quartile_tract.csv', delimiter = ",", dtype = int)
CA_TRACT = pd.DataFrame(data = {'Population': Population, 'HPIQuartile': Quartile})

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

gamma = int(np.ceil(0.84 * total_population / num_current_stores))

###########################################################################

### Demand function
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

### Import solution
path = '../Result/Tract_0.7capacity_N10/'

y_current = np.genfromtxt(path + 'Dist/y_current.csv', delimiter = ",", dtype = float)
y_current_hpi = np.genfromtxt(path + 'HPI_Dist/y_current.csv', delimiter = ",", dtype = float)
y_total = np.genfromtxt(path + 'Dist/y_total.csv', delimiter = ",", dtype = float)
y_total_hpi = np.genfromtxt(path + 'HPI_Dist/y_total.csv', delimiter = ",", dtype = float)

z_current = np.genfromtxt(path + 'Dist/z_current.csv', delimiter = ",", dtype = float)
z_current_hpi = np.genfromtxt(path + 'HPI_Dist/z_current.csv', delimiter = ",", dtype = float)
z_total = np.genfromtxt(path + 'Dist/z_total.csv', delimiter = ",", dtype = float)
z_total_hpi = np.genfromtxt(path + 'HPI_Dist/z_total.csv', delimiter = ",", dtype = float)

# Matrix form
mat_y_current = np.reshape(y_current, (num_zips, num_current_stores))
mat_y_current_hpi = np.reshape(y_current_hpi, (num_zips, num_current_stores))
mat_y_total = np.reshape(y_total, (num_zips, num_total_stores))
mat_y_total_hpi = np.reshape(y_total_hpi, (num_zips, num_total_stores))

###########################################################################

### Stores selected
Current['Selected_Current_Dist'] = z_current
Current['Selected_Current_DistHPI'] = z_current_hpi
Current['Selected_Total_Dist'] = z_total[0:num_current_stores]
Current['Selected_Total_DistHPI'] = z_total_hpi[0:num_current_stores]

Dollar['Selected_Total_Dist'] = z_total[num_current_stores:num_total_stores]
Dollar['Selected_Total_DistHPI'] = z_total_hpi[num_current_stores:num_total_stores]

###########################################################################

### Utilization (total demand/capacity)

# Exceeds 1 as the capacity constraint is based on F_D
Current['Utilization_Current_Dist'] = np.multiply(F_DH_current, mat_y_current).T @ Population / gamma
Current['Utilization_Current_DistHPI'] = np.multiply(F_DH_current, mat_y_current_hpi).T @ Population / gamma
Current['Utilization_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[:,0:num_current_stores].T @ Population / gamma
Current['Utilization_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[:,0:num_current_stores].T @ Population / gamma

Dollar['Utilization_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[:,num_current_stores:num_total_stores].T @ Population / gamma
Dollar['Utilization_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[:,num_current_stores:num_total_stores].T @ Population / gamma

###########################################################################

### Utilzation (demand/capacity) by HPI

# Population
pop1 = Population[CA_TRACT['HPIQuartile'] == 1]
pop2 = Population[CA_TRACT['HPIQuartile'] == 2]
pop3 = Population[CA_TRACT['HPIQuartile'] == 3]
pop4 = Population[CA_TRACT['HPIQuartile'] == 4]

# Current
Current['Utilization_HPI1_Current_Dist'] = np.multiply(F_DH_current, mat_y_current)[CA_TRACT['HPIQuartile'] == 1].T @ pop1 / gamma
Current['Utilization_HPI1_Current_DistHPI'] = np.multiply(F_DH_current, mat_y_current_hpi)[CA_TRACT['HPIQuartile'] == 1].T @ pop1 / gamma
Current['Utilization_HPI1_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[CA_TRACT['HPIQuartile'] == 1][:,0:num_current_stores].T @ pop1 / gamma
Current['Utilization_HPI1_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[CA_TRACT['HPIQuartile'] == 1][:,0:num_current_stores].T @ pop1 / gamma

Current['Utilization_HPI2_Current_Dist'] = np.multiply(F_DH_current, mat_y_current)[CA_TRACT['HPIQuartile'] == 2].T @ pop2 / gamma
Current['Utilization_HPI2_Current_DistHPI'] = np.multiply(F_DH_current, mat_y_current_hpi)[CA_TRACT['HPIQuartile'] == 2].T @ pop2 / gamma
Current['Utilization_HPI2_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[CA_TRACT['HPIQuartile'] == 2][:,0:num_current_stores].T @ pop2 / gamma
Current['Utilization_HPI2_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[CA_TRACT['HPIQuartile'] == 2][:,0:num_current_stores].T @ pop2 / gamma

Current['Utilization_HPI3_Current_Dist'] = np.multiply(F_DH_current, mat_y_current)[CA_TRACT['HPIQuartile'] == 3].T @ pop3 / gamma
Current['Utilization_HPI3_Current_DistHPI'] = np.multiply(F_DH_current, mat_y_current_hpi)[CA_TRACT['HPIQuartile'] == 3].T @ pop3 / gamma
Current['Utilization_HPI3_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[CA_TRACT['HPIQuartile'] == 3][:,0:num_current_stores].T @ pop3 / gamma
Current['Utilization_HPI3_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[CA_TRACT['HPIQuartile'] == 3][:,0:num_current_stores].T @ pop3 / gamma

Current['Utilization_HPI4_Current_Dist'] = np.multiply(F_DH_current, mat_y_current)[CA_TRACT['HPIQuartile'] == 4].T @ pop4 / gamma
Current['Utilization_HPI4_Current_DistHPI'] = np.multiply(F_DH_current, mat_y_current_hpi)[CA_TRACT['HPIQuartile'] == 4].T @ pop4 / gamma
Current['Utilization_HPI4_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[CA_TRACT['HPIQuartile'] == 4][:,0:num_current_stores].T @ pop4 / gamma
Current['Utilization_HPI4_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[CA_TRACT['HPIQuartile'] == 4][:,0:num_current_stores].T @ pop4 / gamma

# Dollar
Dollar['Utilization_HPI1_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[CA_TRACT['HPIQuartile'] == 1][:,num_current_stores:num_total_stores].T @ pop1 / gamma
Dollar['Utilization_HPI1_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[CA_TRACT['HPIQuartile'] == 1][:,num_current_stores:num_total_stores].T @ pop1 / gamma

Dollar['Utilization_HPI2_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[CA_TRACT['HPIQuartile'] == 2][:,num_current_stores:num_total_stores].T @ pop2 / gamma
Dollar['Utilization_HPI2_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[CA_TRACT['HPIQuartile'] == 2][:,num_current_stores:num_total_stores].T @ pop2 / gamma

Dollar['Utilization_HPI3_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[CA_TRACT['HPIQuartile'] == 3][:,num_current_stores:num_total_stores].T @ pop3 / gamma
Dollar['Utilization_HPI3_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[CA_TRACT['HPIQuartile'] == 3][:,num_current_stores:num_total_stores].T @ pop3 / gamma

Dollar['Utilization_HPI4_Total_Dist'] = np.multiply(F_DH_total, mat_y_total)[CA_TRACT['HPIQuartile'] == 4][:,num_current_stores:num_total_stores].T @ pop4 / gamma
Dollar['Utilization_HPI4_Total_DistHPI'] = np.multiply(F_DH_total, mat_y_total_hpi)[CA_TRACT['HPIQuartile'] == 4][:,num_current_stores:num_total_stores].T @ pop4 / gamma


###########################################################################

### Export
Current.to_csv(path + 'Current.csv', index = False)
Dollar.to_csv(path + 'Dollar.csv', index = False)


###########################################################################

###########################################################################

###########################################################################

###########################################################################


import os
import pandas as pd
import numpy as np
from tabulate import tabulate

os.chdir('/Users/jingyuanhu/Desktop/Research/COVID project/Submission MS/Code')

###########################################################################

### Store table under the special case: fixed active stores in each county ###

TRACT_RAW = pd.read_csv('../Data/Tract_CA.csv', delimiter = ",")
Population = np.genfromtxt('../Data/population_tract.csv', delimiter = ",", dtype = int)
total_population = sum(Population)
Quartile = np.genfromtxt('../Data/quartile_tract.csv', delimiter = ",", dtype = int)
CA_TRACT = pd.DataFrame(data = {'FIPS': TRACT_RAW['FIPS'],
                                'County': TRACT_RAW['COUNTY'],
                                'County_name': TRACT_RAW['County_name'],
                                'Tract': TRACT_RAW['TRACT'],
                                'Latitude': TRACT_RAW['LATITUDE'],
                                'Longitude': TRACT_RAW['LONGITUDE'],
                                'Population': Population, 'HPIQuartile': Quartile})
    
CURRENT = pd.read_csv('../Data/Current_stores_CA.csv', delimiter = ",")
DOLLAR = pd.read_csv('../Data/Dollar_stores_CA.csv', delimiter = ",")

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

### Import optimization solution
path = '../Result/Tract_const/'

y_total_hpi = np.genfromtxt(path + 'HPI_Dist/y_total.csv', delimiter = ",", dtype = float)
z_total_hpi = np.genfromtxt(path + 'HPI_Dist/z_total.csv', delimiter = ",", dtype = float)
mat_y_total_hpi = np.reshape(y_total_hpi, (num_zips, num_total_stores))

CURRENT_SELECTED = CURRENT[(z_total_hpi[0:num_current_stores] == 1)]
DOLLAR_SELECTED = DOLLAR[(z_total_hpi[num_current_stores:num_total_stores] == 1)]

###########################################################################

### Number of stores in each county & indicator arrays
county_table = []
for county in CA_TRACT['County_name'].unique():
    
    # active stores
    county_active_stores = CURRENT[CURRENT['County'] == county].shape[0]
    county_active_stores1 = CURRENT[(CURRENT['County'] == county) & (CURRENT['HPIQuartile'] == 1)].shape[0]
    county_active_stores2 = CURRENT[(CURRENT['County'] == county) & (CURRENT['HPIQuartile'] == 2)].shape[0]
    county_active_stores3 = CURRENT[(CURRENT['County'] == county) & (CURRENT['HPIQuartile'] == 3)].shape[0]
    county_active_stores4 = CURRENT[(CURRENT['County'] == county) & (CURRENT['HPIQuartile'] == 4)].shape[0]
    
    # pharmacies
    county_current_stores = CURRENT_SELECTED[CURRENT_SELECTED['County'] == county].shape[0]
    county_current_stores1 = CURRENT_SELECTED[(CURRENT_SELECTED['County'] == county) & (CURRENT_SELECTED['HPIQuartile'] == 1)].shape[0]
    county_current_stores2 = CURRENT_SELECTED[(CURRENT_SELECTED['County'] == county) & (CURRENT_SELECTED['HPIQuartile'] == 2)].shape[0]
    county_current_stores3 = CURRENT_SELECTED[(CURRENT_SELECTED['County'] == county) & (CURRENT_SELECTED['HPIQuartile'] == 3)].shape[0]
    county_current_stores4 = CURRENT_SELECTED[(CURRENT_SELECTED['County'] == county) & (CURRENT_SELECTED['HPIQuartile'] == 4)].shape[0]
    
    # dollar stores
    county_dollar_stores = DOLLAR_SELECTED[DOLLAR_SELECTED['County'] == county].shape[0]
    county_dollar_stores1 = DOLLAR_SELECTED[(DOLLAR_SELECTED['County'] == county) & (DOLLAR_SELECTED['HPIQuartile'] == 1)].shape[0]
    county_dollar_stores2 = DOLLAR_SELECTED[(DOLLAR_SELECTED['County'] == county) & (DOLLAR_SELECTED['HPIQuartile'] == 2)].shape[0]
    county_dollar_stores3 = DOLLAR_SELECTED[(DOLLAR_SELECTED['County'] == county) & (DOLLAR_SELECTED['HPIQuartile'] == 3)].shape[0]
    county_dollar_stores4 = DOLLAR_SELECTED[(DOLLAR_SELECTED['County'] == county) & (DOLLAR_SELECTED['HPIQuartile'] == 4)].shape[0]
    
    # whether a current stores belongs to this county
    county_table.append({'Name': county, 'Num active stores': county_active_stores, 'Num active stores 1': county_active_stores1, 
                         'Num active stores 2': county_active_stores2, 'Num active stores 3': county_active_stores3,
                         'Num active stores 4': county_active_stores4, 'Num pharmacy selected': county_current_stores,
                         'Num pharmacy selected1': county_current_stores1, 'Num pharmacy selected2': county_current_stores2,
                         'Num pharmacy selected3': county_current_stores3, 'Num pharmacy selected4': county_current_stores4,
                         'Num dollar selected': county_dollar_stores, 'Num dollar selected1': county_dollar_stores1,
                         'Num dollar selected2': county_dollar_stores2, 'Num dollar selected3': county_dollar_stores3,
                         'Num dollar selected4': county_dollar_stores4})
        
county_table = pd.DataFrame(county_table)

print(tabulate(county_table, tablefmt="latex", showindex=False))

