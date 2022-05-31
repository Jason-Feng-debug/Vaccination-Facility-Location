#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28, 2022
@Author: Jingyuan Hu

INPUT: Zip-code level data, Distance matrix
OUTPUT: Optimal store selection
"""

import os
import pandas as pd
import numpy as np
os.chdir('/Users/jingyuanhu/Desktop/Research/COVID project/Submission MS/Code')
from utils import optimize, optimize_constant
scale_factor = 10000

def main():
    
    print('Start importing the problem...')
    
    ###########################################################################
    
    ### Census Tract
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
    
    ### Current ###
    C_current = np.genfromtxt('../Data/dist_matrix_CA_current_tract.csv', delimiter = ",", dtype = float)
    C_current = C_current.astype(int)
    C_current = C_current.T
    num_zips, num_current_stores = np.shape(C_current)
       
    ### Dollar ###
    C_dollar = np.genfromtxt('../Data/dist_matrix_CA_dollar_tract.csv', delimiter = ",", dtype = float)
    C_dollar = C_dollar.astype(int)
    C_dollar = C_dollar.T
    num_zips, num_dollar_stores = np.shape(C_dollar)
    
    ### Total ###
    C_total = np.concatenate((C_current, C_dollar), axis = 1)
    num_total_stores = num_current_stores + num_dollar_stores
    
    ###########################################################################
    
    ### Travel to the closest N stores only
    N = 10
    Closest_current = np.ones((num_zips, num_current_stores))
    Closest_total = np.ones((num_zips, num_total_stores))
    np.put_along_axis(Closest_current, np.argpartition(C_current,N,axis=1)[:,N:],0,axis=1)
    np.put_along_axis(Closest_total, np.argpartition(C_total,N,axis=1)[:,N:],0,axis=1)
    
    ### Newly added dollar does not affect current rank
    Closest_total_dollar = np.ones((num_zips, num_dollar_stores))
    np.put_along_axis(Closest_total_dollar, np.argpartition(C_dollar,N,axis=1)[:,N:],0,axis=1)    
    Closest_total_dollar = np.concatenate((Closest_current, Closest_total_dollar), axis = 1)
    
    Closest_current = Closest_current.flatten()
    Closest_total = Closest_total.flatten()
    Closest_total_dollar = Closest_total_dollar.flatten()
            
    ###########################################################################
    
    ### Willingness based on distance ###
    F_D_total = 0.755 - 0.069 * np.log(C_total/1000)
    F_D_current = F_D_total[:,0:num_current_stores]
    
    ### Based on distance and HPI
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
    
    # 0.8 is the rate for at least one dose
    gamma = int(np.ceil(0.7 * total_population / num_current_stores))
        
    ###########################################################################
    
    ### Number of stores in each county & indicator arrays
    county_table = []
    for county in CA_TRACT['County_name'].unique():
        # number of current stores
        county_current_stores = CURRENT[CURRENT['County'] == county].shape[0]
        # whether a current stores belongs to this county
        indicator_current = (CURRENT['County'] == county).values.astype(int)
        indicator_dollar = (DOLLAR['County'] == county).values.astype(int)
        indicator = np.concatenate((indicator_current, indicator_dollar), axis=None)
        county_table.append({'Name': county, 'Num_stores': county_current_stores, 'Indicator': indicator})
        
    county_table = pd.DataFrame(county_table)
    
    ###########################################################################
        
    print('Constructing demand vectors...')
    
    # n copies of demand
    p_total = np.tile(Population, num_total_stores)
    p_total = np.reshape(p_total, (num_total_stores, num_zips))
    p_total = p_total.T.flatten()
       
    p_current = np.tile(Population, num_current_stores)
    p_current = np.reshape(p_current, (num_current_stores, num_zips))
    p_current = p_current.T.flatten()
    
    # travel distance
    c_current = C_current.flatten() / scale_factor
    c_total = C_total.flatten() / scale_factor
    
    f_d_current = F_D_current.flatten()
    f_d_total = F_D_total.flatten()
    
    f_dh_current = F_DH_current.flatten()
    f_dh_total = F_DH_total.flatten()
    
    # population * distance 
    pc_current = p_current * c_current
    pc_total = p_total * c_total
    
    # population * willingness
    pfd_current = p_current * f_d_current
    pfd_total = p_total * f_d_total
    
    pfdh_current = p_current * f_dh_current
    pfdh_total = p_total * f_dh_total
    
    del C_current, C_dollar, C_total, F_D_total, F_D_current, F_DH_total, F_DH_current
    
    ###########################################################################
    
    ### Current, Dist ###
    # optimize(scenario = 'current', demand = 'dist',
    #           pc = pc_current, pf = pfd_current, ncp = p_current, p = Population,
    #           closest = Closest_current, gamma=gamma, num_current_stores=num_current_stores,
    #           num_total_stores=num_total_stores, num_zips=num_zips, scale_factor=scale_factor)
    
    ### Current, DistHPI ###
    # optimize(scenario = 'current', demand = 'HPI_dist',
    #           pc = pc_current, pf = pfdh_current, ncp = p_current, p = Population,
    #           closest = Closest_current, gamma=gamma, num_current_stores=num_current_stores,
    #           num_total_stores=num_total_stores, num_zips=num_zips, scale_factor=scale_factor)
    
    ### Total, Dist ###
    # optimize(scenario = 'total', demand = 'dist',
    #           pc = pc_total, pf = pfd_total, ncp = p_total, p = Population,
    #           closest = Closest_total, gamma=gamma, num_current_stores=num_current_stores,
    #           num_total_stores=num_total_stores, num_zips=num_zips, scale_factor=scale_factor)
    
    ### Total, DistHPI ###
    # optimize(scenario = 'total', demand = 'HPI_dist',
    #           pc = pc_total, pf = pfdh_total, ncp = p_total, p = Population, 
    #           closest = Closest_total, gamma=gamma, num_current_stores=num_current_stores,
    #           num_total_stores=num_total_stores, num_zips=num_zips, scale_factor=scale_factor)
    
    ###########################################################################
    
    ### Fix total supply, different budget & capacity ###
    # budget_stores_list = np.array([3285, 3535, 3785, 4035, 4285, 4535])
    # for budget_stores in budget_stores_list:
        
    #     gamma = int(np.ceil(0.7 * total_population / budget_stores))
        
    #     optimize(scenario = 'current', demand = 'HPI_dist',
    #               pc = pc_current, pf = pfdh_current, ncp = p_current, p = Population,
    #               closest = Closest_current, gamma=gamma, num_current_stores=num_current_stores,
    #               num_total_stores=num_total_stores, num_zips=num_zips, budget_stores = budget_stores,
    #               scale_factor=scale_factor)
        
    #     optimize(scenario = 'total', demand = 'HPI_dist', 
    #               pc = pc_total, pf = pfdh_total, ncp = p_total, p = Population, 
    #               closest = Closest_total, gamma=gamma, num_current_stores=num_current_stores,
    #               num_total_stores=num_total_stores, num_zips=num_zips, budget_stores = budget_stores,
    #               scale_factor=scale_factor)

    ###########################################################################
    
    ### Keep current, open dollar stores ###
    ### Also want to keep the current closest
    # num_dollar_list = np.array([20, 50])
    # for num_new_dollar_stores in num_dollar_list:
    #     optimize(scenario = 'total', demand = 'HPI_dist', 
    #              pc = pc_total, pf = pfdh_total, ncp = p_total, p = Population, 
    #              closest = Closest_total_dollar, gamma=gamma, num_current_stores=num_current_stores,
    #              num_total_stores=num_total_stores, num_zips=num_zips,
    #              budget_stores = num_current_stores + num_new_dollar_stores,
    #              scale_factor=scale_factor)
    
    ###########################################################################
    
    ### Keep number of stores fixed in each county ###
    # NOTE: we don't need to run the model for current
    optimize_constant(scenario = 'total', demand = 'HPI_dist',
                      pc = pc_total, pf = pfdh_total, ncp = p_total, p = Population, 
                      gamma=gamma, closest=Closest_total, num_current_stores=num_current_stores, 
                      num_total_stores=num_total_stores, num_zips=num_zips, 
                      county_table=county_table, scale_factor=scale_factor)
    
    
if __name__ == "__main__":
    main()