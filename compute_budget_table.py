#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 18, 2022
@author: Jingyuan Hu
"""

import os
import pandas as pd
import numpy as np
from tabulate import tabulate

os.chdir('/Users/jingyuanhu/Desktop/Research/COVID project/Submission MS/Code')

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
result_list = []

path = '../Result/Tract_0.7_budget/'

budget_stores_list = np.array([3285, 3535, 3785, 4035])
for budget_stores in budget_stores_list:
        
        # Import
        y_current_hpi = np.genfromtxt(path + str(budget_stores) + '/HPI_Dist/y_current.csv', delimiter = ",", dtype = float)
        y_total_hpi = np.genfromtxt(path + str(budget_stores) + '/HPI_Dist/y_total.csv', delimiter = ",", dtype = float)
        mat_y_current_hpi = np.reshape(y_current_hpi, (num_zips, num_current_stores))
        mat_y_total_hpi = np.reshape(y_total_hpi, (num_zips, num_total_stores))
        
        # Rate
        rate_current_hpi = np.sum(np.multiply(F_DH_current, mat_y_current_hpi), axis = 1)
        rate_total_hpi = np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1)      
        CA_TRACT['Rate_Current_HPI'] = rate_current_hpi
        CA_TRACT['Rate_Total_HPI'] = rate_total_hpi
        CA_TRACT['Vaccinated_Population_Current_HPI'] = CA_TRACT['Rate_Current_HPI'] * CA_TRACT['Population']
        CA_TRACT['Vaccinated_Population_Total_HPI'] = CA_TRACT['Rate_Total_HPI'] * CA_TRACT['Population']

        # rate_current_hpi = round(sum(CA_TRACT['Vaccinated_Population_Current_HPI'].values) / total_population * 100,2)
        # rate_current_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Vaccinated_Population_Current_HPI'].values) / population1 * 100,2)
        # rate_current_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Vaccinated_Population_Current_HPI'].values) / population2 * 100,2)
        # rate_current_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Vaccinated_Population_Current_HPI'].values) / population3 * 100,2)
        # rate_current_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Vaccinated_Population_Current_HPI'].values) / population4 * 100,2)

        # rate_total_hpi = round(sum(CA_TRACT['Vaccinated_Population_Total_HPI'].values) / total_population * 100,2)
        # rate_total_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI'].values) / population1 * 100,2)
        # rate_total_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI'].values) / population2 * 100,2)
        # rate_total_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI'].values) / population3 * 100,2)
        # rate_total_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI'].values) / population4 * 100,2)
        
        rate_current_hpi = round(sum(CA_TRACT['Vaccinated_Population_Current_HPI'].values) / 1000000,2)
        rate_current_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Vaccinated_Population_Current_HPI'].values) / 1000000,2)
        rate_current_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Vaccinated_Population_Current_HPI'].values) / 1000000,2)
        rate_current_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Vaccinated_Population_Current_HPI'].values) / 1000000,2)
        rate_current_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Vaccinated_Population_Current_HPI'].values) / 1000000,2)

        rate_total_hpi = round(sum(CA_TRACT['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        rate_total_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        rate_total_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        rate_total_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        rate_total_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        
        # Dist
        avg_dist_current_hpi = np.nan_to_num(np.sum(np.multiply(C_current, mat_y_current_hpi), axis = 1) / np.sum(mat_y_current_hpi, axis = 1), posinf=0)
        avg_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(C_total, mat_y_total_hpi), axis = 1) / np.sum(mat_y_total_hpi, axis = 1), posinf=0)
        CA_TRACT['Dist_Current_HPI'] = avg_dist_current_hpi
        CA_TRACT['Dist_Total_HPI'] = avg_dist_total_hpi
        CA_TRACT['Allocated_Population_Current_HPI'] = np.sum(mat_y_current_hpi, axis = 1) * CA_TRACT['Population']
        CA_TRACT['Allocated_Population_Total_HPI'] = np.sum(mat_y_total_hpi, axis = 1) * CA_TRACT['Population']
        CA_TRACT['Dist_Current_HPI_weighted'] = CA_TRACT['Dist_Current_HPI'] * CA_TRACT['Allocated_Population_Current_HPI']
        CA_TRACT['Dist_Total_HPI_weighted'] = CA_TRACT['Dist_Total_HPI'] * CA_TRACT['Allocated_Population_Total_HPI']

        avg_dist_current_hpi = round(sum(CA_TRACT['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT['Allocated_Population_Current_HPI'].values))
        avg_dist_current_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Allocated_Population_Current_HPI']))
        avg_dist_current_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Allocated_Population_Current_HPI']))
        avg_dist_current_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Allocated_Population_Current_HPI']))
        avg_dist_current_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Allocated_Population_Current_HPI']))
        
        avg_dist_total_hpi = round(sum(CA_TRACT['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT['Allocated_Population_Total_HPI'].values))
        avg_dist_total_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Allocated_Population_Total_HPI']))
        avg_dist_total_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Allocated_Population_Total_HPI']))
        avg_dist_total_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Allocated_Population_Total_HPI']))
        avg_dist_total_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Allocated_Population_Total_HPI']))
        
        # Actual Dist
        actual_dist_current_hpi = np.nan_to_num(np.sum(np.multiply(F_DH_current, np.multiply(C_current, mat_y_current_hpi)), axis = 1) / np.sum(np.multiply(F_DH_current, mat_y_current_hpi), axis = 1), posinf=0)
        actual_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1) / np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1), posinf=0)
        CA_TRACT['Dist_Current_HPI_Actual'] = actual_dist_current_hpi
        CA_TRACT['Dist_Total_HPI_Actual'] = actual_dist_total_hpi
        CA_TRACT['Dist_Current_HPI_weighted'] = CA_TRACT['Dist_Current_HPI_Actual'] * CA_TRACT['Vaccinated_Population_Current_HPI']
        CA_TRACT['Dist_Total_HPI_weighted'] = CA_TRACT['Dist_Total_HPI_Actual'] * CA_TRACT['Vaccinated_Population_Total_HPI']

        actual_dist_current_hpi = round(sum(CA_TRACT['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT['Vaccinated_Population_Current_HPI'].values))
        actual_dist_current_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Vaccinated_Population_Current_HPI']))
        actual_dist_current_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Vaccinated_Population_Current_HPI']))
        actual_dist_current_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Vaccinated_Population_Current_HPI']))
        actual_dist_current_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Dist_Current_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Vaccinated_Population_Current_HPI']))
        
        actual_dist_total_hpi = round(sum(CA_TRACT['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT['Vaccinated_Population_Total_HPI'].values))
        actual_dist_total_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI']))
        actual_dist_total_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI']))
        actual_dist_total_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI']))
        actual_dist_total_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI']))
        
        # Current
        results = {"Scenario": 'Current', "Number Stores": budget_stores, "Rate": rate_current_hpi, 
                   "Rate HPI1": rate_current_hpi1, "Rate HPI2": rate_current_hpi2, "Rate HPI3": rate_current_hpi3, 
                   "Rate HPI4": rate_current_hpi4, "Dist": avg_dist_current_hpi, "Dist HPI1": avg_dist_current_hpi1,
                   "Dist HPI2": avg_dist_current_hpi2, "Dist HPI3": avg_dist_current_hpi3, "Dist HPI4": avg_dist_current_hpi4,
                   "Actual Dist": actual_dist_current_hpi/1000, "Actual Dist HPI1": actual_dist_current_hpi1/1000, "Actual Dist HPI2": actual_dist_current_hpi2/1000, 
                   "Actual Dist HPI3": actual_dist_current_hpi3/1000, "Actual Dist HPI4": actual_dist_current_hpi4/1000}
        result_list.append(results)
        
        # Both
        results = {"Scenario": 'Both', "Number Stores": budget_stores, "Rate": rate_total_hpi, 
                   "Rate HPI1": rate_total_hpi1, "Rate HPI2": rate_total_hpi2, "Rate HPI3": rate_total_hpi3, 
                   "Rate HPI4": rate_total_hpi4, "Dist": avg_dist_total_hpi, "Dist HPI1": avg_dist_total_hpi1,
                   "Dist HPI2": avg_dist_total_hpi2, "Dist HPI3": avg_dist_total_hpi3, "Dist HPI4": avg_dist_total_hpi4,
                   "Actual Dist": actual_dist_total_hpi/1000, "Actual Dist HPI1": actual_dist_total_hpi1/1000, "Actual Dist HPI2": actual_dist_total_hpi2/1000, 
                   "Actual Dist HPI3": actual_dist_total_hpi3/1000, "Actual Dist HPI4": actual_dist_total_hpi4/1000}
        result_list.append(results)

###########################################################################

budget_stores_list = np.array([4285, 4535])

for budget_stores in budget_stores_list:
        
        # Import
        y_total_hpi = np.genfromtxt(path + str(budget_stores) + '/HPI_Dist/y_total.csv', delimiter = ",", dtype = float)
        mat_y_total_hpi = np.reshape(y_total_hpi, (num_zips, num_total_stores))
        
        # Rate
        rate_total_hpi = np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1)
        CA_TRACT['Rate_Total_HPI'] = rate_total_hpi
        CA_TRACT['Vaccinated_Population_Total_HPI'] = CA_TRACT['Rate_Total_HPI'] * CA_TRACT['Population']

        rate_total_hpi = round(sum(CA_TRACT['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        rate_total_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        rate_total_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        rate_total_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        rate_total_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI'].values) / 1000000,2)
        
        
        # Dist
        avg_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(C_total, mat_y_total_hpi), axis = 1) / np.sum(mat_y_total_hpi, axis = 1), posinf=0)
        CA_TRACT['Dist_Total_HPI'] = avg_dist_total_hpi
        CA_TRACT['Allocated_Population_Total_HPI'] = np.sum(mat_y_total_hpi, axis = 1) * CA_TRACT['Population']
        CA_TRACT['Dist_Total_HPI_weighted'] = CA_TRACT['Dist_Total_HPI'] * CA_TRACT['Allocated_Population_Total_HPI']
        
        avg_dist_total_hpi = round(sum(CA_TRACT['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT['Allocated_Population_Total_HPI'].values))
        avg_dist_total_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Allocated_Population_Total_HPI']))
        avg_dist_total_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Allocated_Population_Total_HPI']))
        avg_dist_total_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Allocated_Population_Total_HPI']))
        avg_dist_total_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Allocated_Population_Total_HPI']))
         
        # Actual Dist
        actual_dist_total_hpi = np.nan_to_num(np.sum(np.multiply(F_DH_total, np.multiply(C_total, mat_y_total_hpi)), axis = 1) / np.sum(np.multiply(F_DH_total, mat_y_total_hpi), axis = 1), posinf=0)
        CA_TRACT['Dist_Total_HPI_Actual'] = actual_dist_total_hpi
        CA_TRACT['Dist_Total_HPI_weighted'] = CA_TRACT['Dist_Total_HPI_Actual'] * CA_TRACT['Vaccinated_Population_Total_HPI']

        actual_dist_total_hpi = round(sum(CA_TRACT['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT['Vaccinated_Population_Total_HPI'].values))
        actual_dist_total_hpi1 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 1]['Vaccinated_Population_Total_HPI']))
        actual_dist_total_hpi2 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 2]['Vaccinated_Population_Total_HPI']))
        actual_dist_total_hpi3 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 3]['Vaccinated_Population_Total_HPI']))
        actual_dist_total_hpi4 = round(sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Dist_Total_HPI_weighted'].values) / sum(CA_TRACT[CA_TRACT['HPIQuartile'] == 4]['Vaccinated_Population_Total_HPI']))
        
        results = {"Scenario": 'Both', "Number Stores": budget_stores, "Rate": rate_total_hpi, 
                   "Rate HPI1": rate_total_hpi1, "Rate HPI2": rate_total_hpi2, "Rate HPI3": rate_total_hpi3, 
                   "Rate HPI4": rate_total_hpi4, "Dist": avg_dist_total_hpi, "Dist HPI1": avg_dist_total_hpi1,
                   "Dist HPI2": avg_dist_total_hpi2, "Dist HPI3": avg_dist_total_hpi3, "Dist HPI4": avg_dist_total_hpi4,
                   "Actual Dist": actual_dist_total_hpi/1000, "Actual Dist HPI1": actual_dist_total_hpi1/1000, "Actual Dist HPI2": actual_dist_total_hpi2/1000, 
                   "Actual Dist HPI3": actual_dist_total_hpi3/1000, "Actual Dist HPI4": actual_dist_total_hpi4/1000}
        result_list.append(results)

result_table = pd.DataFrame(result_list)
result_table.to_csv(path + 'result_table.csv', encoding='utf-8', index=False, header = True)

print(tabulate(result_table, tablefmt="latex"))