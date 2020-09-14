# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:18:53 2020

@author: Dogukan
"""
import numpy as np

def create_mcar_single(df, missing_column, p_missing, random_state=709):
    np.random.seed(random_state)
    indices = [df.sample(n = 1).index[0] for i in range(round(p_missing * df.shape[0]))]
    while len(set(indices)) < round(p_missing * df.shape[0]):
        indices.append(df.sample(n = 1).index[0])
    mcar_column = [1 if i in indices else 0 for i in range(df.shape[0])]
    
    df_new = df.copy()
    for i in range(len(mcar_column)):
        if mcar_column[i] == 1:
            df_new[missing_column][i] = '?'      
    df_new = df_new.replace('?', np.nan)
    return df_new

def create_mcar_mult(df, mising_column, p_missing, random_state):
    df_new = df.copy()
    for i in range(len(mising_column)):
        tmp = create_mcar_single(df, mising_column[i], p_missing, random_state=random_state+i)
        df_new[mising_column[i]] = tmp[mising_column[i]] 
    return df_new

def create_mcar(df, missing_column, p_missing, random_state=709):
    if (type(missing_column) == str):
        df_new = create_mcar_single(df, missing_column, p_missing, random_state=709)
    elif (type(missing_column) == list):
        df_new = create_mcar_mult(df, missing_column, p_missing, random_state=709)
    else:
        raise Exception('Name of the columns should be given as either str or list. Given format was {}'.format(
            type(missing_column)))
    return df_new

def test_mcar_single(df, missing_column, p_missing):
    if (df[missing_column].isna().sum() == round(p_missing * df.shape[0])):
        print('Missingness created for', missing_column ,'succesfully!')
    else:
        print('Something is wrong.')
        
def test_mcar_mult(df, missing_column, p_missing):
    for i in range(len(missing_column)):
        test_mcar_single(df, missing_column[i], p_missing)

def test_mcar(df, missing_column, p_missing):
    if (type(missing_column) == str):
        result = test_mcar_single(df, missing_column, p_missing)
    elif (type(missing_column) == list):
        result = test_mcar_mult(df, missing_column, p_missing)
    return(result)        