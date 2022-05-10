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
os.chdir('/Users/jingyuanhu/Desktop/Research/COVID_project/Submission MS/Code')
from utils import optimize
scale_factor = 10000

def main():
    
    print('Start importing the problem...')
    
    ### Zip   
    # CA_ZIP = pd.read_csv('../Data/CaliforniaZipHPI.csv', delimiter = ",") 
    # Population = CA_ZIP['Population'].values
    # total_population = sum(Population)
    # Quartile = CA_ZIP['HPIQuartile'].values.astype(int)
    
    ### Current ###
    # C_current = np.genfromtxt('../Data/dist_matrix_CA_current.csv', delimiter = ",", dtype = float)
    # C_current = C_current.astype(int)
    # C_current = C_current.T
    # num_zips, num_current_stores = np.shape(C_current)
       
    ### Dollar ###
    # C_dollar = np.genfromtxt('../Data/dist_matrix_CA_dollar.csv', delimiter = ",", dtype = float)
    # C_dollar = C_dollar.astype(int)
    # C_dollar = C_dollar.T
    # num_zips, num_dollar_stores = np.shape(C_dollar)
    
    ### Total ###
    # C_total = np.concatenate((C_current, C_dollar), axis = 1)
    # num_total_stores = num_current_stores + num_dollar_stores
    
    ###########################################################################
    
    ### Census Tract
    Population = np.genfromtxt('../Data/population_tract.csv', delimiter = ",", dtype = int)
    total_population = sum(Population)
    Quartile = np.genfromtxt('../Data/quartile_tract.csv', delimiter = ",", dtype = int)
    
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
    
    # test_current = Closest_current * C_current
    # test_total = Closest_total * C_total
    
    # max_current = np.max(test_current, axis = 1)
    # max_total = np.max(test_total, axis = 1)
    
    Closest_current = Closest_current.flatten()
    Closest_total = Closest_total.flatten()
        
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
    gamma = int(np.ceil(0.84 * total_population / num_current_stores))
    
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
    
    ### Case I ###
    optimize(scenario = 'current', demand = 'dist',
              pc = pc_current, pf = pfd_current, ncp = p_current, p = Population,
              closest = Closest_current, gamma=gamma, num_current_stores=num_current_stores,
              num_total_stores=num_total_stores, num_zips=num_zips, scale_factor=scale_factor)
    
    ### Test Case ###
    optimize(scenario = 'current', demand = 'HPI_dist',
              pc = pc_current, pf = pfdh_current, ncp = p_current, p = Population,
              closest = Closest_current, gamma=gamma, num_current_stores=num_current_stores,
              num_total_stores=num_total_stores, num_zips=num_zips, scale_factor=scale_factor)
    
    ### Case II ###
    optimize(scenario = 'total', demand = 'dist',
              pc = pc_total, pf = pfd_total, ncp = p_total, p = Population,
              closest = Closest_total, gamma=gamma, num_current_stores=num_current_stores,
              num_total_stores=num_total_stores, num_zips=num_zips, scale_factor=scale_factor)
    
    ### Case III ###
    optimize(scenario = 'total', demand = 'HPI_dist',
              pc = pc_total, pf = pfdh_total, ncp = p_total, p = Population, 
              closest = Closest_total, gamma=gamma, num_current_stores=num_current_stores,
              num_total_stores=num_total_stores, num_zips=num_zips, scale_factor=scale_factor)
    
    
    


if __name__ == "__main__":
    main()