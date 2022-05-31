#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28, 2022
@Author: Jingyuan Hu 
"""

import time
import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB, quicksum

def optimize(scenario, demand, pc, pf, ncp, p, gamma, closest,
             num_current_stores, num_total_stores, num_zips, 
             scale_factor, budget_stores = 0):
    
    """
    Parameters
    ----------
    scenario : string
        "current": current stores only
        "total": current and dollar stores
        
    demand : string
        "dist": distance only
        "HPI_dist": both HPI and distance
        
    pc : array
        scaled population * distance
    
    pf : array
        scaled population * willingness
        
    ncp : array
        n copies of population vector
        
    p : array
        population vector
        
    closest : array
        0-1 vector that indicates if (i,j) is the nth closest pair
    
    gamma : scalar
        capacity of a single site
        
    budget_stores : scalar
        number of stores to selected
        
    scale_factor : scalar
        scale the value down by a factor to ensure computational feasibility
    """
    
    if demand == 'dist':
        path = '../Result/Tract/Dist/'
    else:
        path = '../Result/Tract/HPI_Dist/'
        
        
    print('Start solving the problem')
    start = time.time()
    m = gp.Model("Vaccination")
    m.Params.IntegralityFocus = 1
    m.Params.MIPGap = 5e-3
    
    total_demand = sum(p)
    
    if scenario == "current":
        num_stores = num_current_stores
    elif scenario == "total":
        num_stores = num_total_stores
    else:
        print('Scenario cannot be identified')
    
    
    ### Variables ###
    z = m.addVars(num_stores, vtype=GRB.BINARY, name = 'z')
    y = m.addVars(num_zips * num_stores, lb = 0, ub = 1, name = 'y')
    
    
    ### Objective ###
    print('Constructing objective function')
    m.setObjective(quicksum(pf[k] * y[k] for k in range(num_zips * num_stores)), gp.GRB.MAXIMIZE)
    
    
    ### Constraints ###
    print('Constructing capacity constraints')
    for j in range(num_stores):
        m.addConstr(quicksum(pf[i * num_stores + j] * y[i * num_stores + j] for i in range(num_zips)) <= gamma * z[j])
    
    print('Constructing demand constraints')
    for i in range(num_zips):
        m.addConstr(quicksum(y[i * num_stores + j] for j in range(num_stores)) <= 1)
    
    print('Constructing budget constraint')
    m.addConstr(z.sum() == num_current_stores, name = 'N')
    # New constraint: keep all current stores
    # m.addConstr(z.sum() == budget_stores, name = 'N')
    # m.addConstr(quicksum(z[j] for j in range(num_current_stores)) == num_current_stores)
    
    
    print('Constructing closest constraint')
    for k in range(num_zips * num_stores):
        m.addConstr(y[k] <= closest[k])

    ### Solve ###
    m.update()
    m.optimize()
    
    ### Export ###
    z_soln = np.zeros(num_stores)
    for j in range(num_stores):
            z_soln[j] = z[j].X

    y_soln = np.zeros(num_zips * num_stores)
    for k in range(num_zips * num_stores):
            y_soln[k] = y[k].X    
    end = time.time()
    
    
    ### Summary ###
    if scenario == "current":
        store_used = sum(z_soln)
        vaccine_rate = pf @ y_soln / total_demand
        avg_dist = (pc @ y_soln / total_demand) * scale_factor    
        allocation_rate = ncp @ y_soln / total_demand
        
        result = [store_used, vaccine_rate, avg_dist, allocation_rate, round(end - start,1)]        
        result_df = pd.DataFrame(result, index =['Stores used', 'Vaccination rate', 'Avg distance', 'Allocation rate', 'Time'],\
                                 columns =['Value'])
        
        np.savetxt(path + 'z_current.csv', z_soln, delimiter=",")
        np.savetxt(path + 'y_current.csv', y_soln, delimiter=",")
        result_df.to_csv(path + 'result_current.csv')
    
    elif scenario == "total":
        store_used = sum(z_soln)
        vaccine_rate = (pf @ y_soln / total_demand)
        avg_dist = (pc @ y_soln / total_demand) * scale_factor    
        allocation_rate = ncp @ y_soln / total_demand
                     
        num_current_store_used = sum(z_soln[0 : num_current_stores])
        num_dollar_store_used = store_used - num_current_store_used
        
        dollar_store_demand = ncp[num_current_stores * num_zips : num_total_stores * num_zips] @ y_soln[num_current_stores * num_zips : num_total_stores * num_zips]
        dollar_store_allocation_rate = dollar_store_demand / total_demand
        
        result = [store_used, vaccine_rate, avg_dist, allocation_rate, num_current_store_used, num_dollar_store_used, dollar_store_allocation_rate, round(end - start,1)]
        result_df = pd.DataFrame(result, index =['Stores used', 'Vaccination rate', 'Avg distance', 'Allocation rate',\
                                                 'Current store used', 'Dollar store used', 'Dollar store allocation rate',\
                                                     'Time'], columns =['Value'])
            
        
        np.savetxt(path + 'z_total.csv', z_soln, delimiter=",")
        np.savetxt(path + 'y_total.csv', y_soln, delimiter=",")
        result_df.to_csv(path + 'result_total.csv')
    
    
    else:
        print('Scenario cannot be identified')
    
    m.dispose()
    
    
    
    

def optimize_constant(scenario, demand, pc, pf, ncp, p, gamma, closest,
                      num_current_stores, num_total_stores, num_zips, 
                      county_table, scale_factor):
    
    """
    Parameters
    ----------
    scenario : string
        "current": current stores only
        "total": current and dollar stores
        
    demand : string
        "dist": distance only
        "HPI_dist": both HPI and distance
        
    pc : array
        scaled population * distance
    
    pf : array
        scaled population * willingness
        
    ncp : array
        n copies of population vector
        
    p : array
        population vector
        
    closest : array
        0-1 vector that indicates if (i,j) is the nth closest pair
    
    gamma : scalar
        capacity of a single site
        
    county_table : pandas dataframe
        county name, number of current stores within, and indicator vector
        
    scale_factor : scalar
        scale the value down by a factor to ensure computational feasibility
    """
    
    if demand == 'dist':
        path = '../Result/Tract_const/Dist/'
    else:
        path = '../Result/Tract_const/HPI_Dist/'
        
        
    print('Start solving the problem')
    start = time.time()
    m = gp.Model("Vaccination")
    m.Params.IntegralityFocus = 1
    m.Params.MIPGap = 5e-3
    
    total_demand = sum(p)
    
    if scenario == "current":
        num_stores = num_current_stores
    elif scenario == "total":
        num_stores = num_total_stores
    else:
        print('Scenario cannot be identified')
    
    
    ### Variables ###
    z = m.addVars(num_stores, vtype=GRB.BINARY, name = 'z')
    y = m.addVars(num_zips * num_stores, lb = 0, ub = 1, name = 'y')
    
    
    ### Objective ###
    print('Constructing objective function')
    m.setObjective(quicksum(pf[k] * y[k] for k in range(num_zips * num_stores)), gp.GRB.MAXIMIZE)
    
    
    ### Constraints ###
    print('Constructing capacity constraints')
    for j in range(num_stores):
        m.addConstr(quicksum(pf[i * num_stores + j] * y[i * num_stores + j] for i in range(num_zips)) <= gamma * z[j])
    
    print('Constructing demand constraints')
    for i in range(num_zips):
        m.addConstr(quicksum(y[i * num_stores + j] for j in range(num_stores)) <= 1)
    
    print('Constructing budget constraint')
    m.addConstr(z.sum() == num_current_stores, name = 'N')
    
    ########################
    
    print('Constructing county budget constraint')
    for county in county_table['Name']:
        num_county_stores = county_table[county_table['Name'] == county]['Num_stores'].values[0]
        indicator = county_table[county_table['Name'] == county]['Indicator'].values[0]        
        m.addConstr(quicksum(z[j] * indicator[j] for j in range(num_stores)) == num_county_stores, name = county)
        
    ########################
    
    print('Constructing closest constraint')
    for k in range(num_zips * num_stores):
        m.addConstr(y[k] <= closest[k])

    ### Solve ###
    m.update()
    m.optimize()
    
    ### Export ###
    z_soln = np.zeros(num_stores)
    for j in range(num_stores):
            z_soln[j] = z[j].X

    y_soln = np.zeros(num_zips * num_stores)
    for k in range(num_zips * num_stores):
            y_soln[k] = y[k].X    
    end = time.time()
    
    
    ### Summary ###
    if scenario == "current":
        store_used = sum(z_soln)
        vaccine_rate = pf @ y_soln / total_demand
        avg_dist = (pc @ y_soln / total_demand) * scale_factor    
        allocation_rate = ncp @ y_soln / total_demand
        
        result = [store_used, vaccine_rate, avg_dist, allocation_rate, round(end - start,1)]        
        result_df = pd.DataFrame(result, index =['Stores used', 'Vaccination rate', 'Avg distance', 'Allocation rate', 'Time'],\
                                 columns =['Value'])
        
        np.savetxt(path + 'z_current.csv', z_soln, delimiter=",")
        np.savetxt(path + 'y_current.csv', y_soln, delimiter=",")
        result_df.to_csv(path + 'result_current.csv')
    
    elif scenario == "total":
        store_used = sum(z_soln)
        vaccine_rate = (pf @ y_soln / total_demand)
        avg_dist = (pc @ y_soln / total_demand) * scale_factor    
        allocation_rate = ncp @ y_soln / total_demand
                     
        num_current_store_used = sum(z_soln[0 : num_current_stores])
        num_dollar_store_used = store_used - num_current_store_used
        
        dollar_store_demand = ncp[num_current_stores * num_zips : num_total_stores * num_zips] @ y_soln[num_current_stores * num_zips : num_total_stores * num_zips]
        dollar_store_allocation_rate = dollar_store_demand / total_demand
        
        result = [store_used, vaccine_rate, avg_dist, allocation_rate, num_current_store_used, num_dollar_store_used, dollar_store_allocation_rate, round(end - start,1)]
        result_df = pd.DataFrame(result, index =['Stores used', 'Vaccination rate', 'Avg distance', 'Allocation rate',\
                                                 'Current store used', 'Dollar store used', 'Dollar store allocation rate',\
                                                     'Time'], columns =['Value'])
            
        
        np.savetxt(path + 'z_total.csv', z_soln, delimiter=",")
        np.savetxt(path + 'y_total.csv', y_soln, delimiter=",")
        result_df.to_csv(path + 'result_total.csv')
    
    
    else:
        print('Scenario cannot be identified')
    
    m.dispose()