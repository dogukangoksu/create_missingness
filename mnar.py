# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:28:34 2020

@author: Dogukan
"""
import numpy as np
import random
from itertools import compress 

def create_mnar_single(df, missing_column, p_missing, threshold, condition):
    
    if condition == 'less':
        np.random.seed(3)
        t = (df[missing_column] <= threshold)
        right_indices = list(compress(range(len(t)), t))
        indices = random.choices(right_indices, k = round(p_missing*df.shape[0]))
        while len(set(indices)) < round(p_missing * df.shape[0]):
            add = random.choice(right_indices)
            indices.append(add)
        mar_column = [1 if i in indices else 0 for i in range(df.shape[0])]
    
    elif condition == 'greater':
        np.random.seed(7)
        t = (df[missing_column] > threshold)
        right_indices = list(compress(range(len(t)), t))
        indices = random.choices(right_indices, k = round(p_missing*df.shape[0]))
        while len(set(indices)) < round(p_missing * df.shape[0]):
            indices.append(random.choice(right_indices))
        mar_column = [1 if i in indices else 0 for i in range(df.shape[0])]

    else:
        raise Exception('Condition must be less or greater. Given condition was: {}'.format(condition))
    
    df_new = df.copy() 
    for i in range(len(mar_column)):
        if mar_column[i] == 1:
            df_new[missing_column][i] = '?'
        
    df_new = df_new.replace('?', np.nan)
    return df_new

def create_mnar_mult(df, missing_column, p_missing, threshold, condition):
    df_new = df.copy()
    for i in range(len(missing_column)):
        tmp = create_mnar_single(df, missing_column[i], p_missing, threshold[i], condition[i])
        df_new[missing_column[i]] = tmp[missing_column[i]] 
    return df_new

def create_mnar(df, missing_column, p_missing, threshold, condition):
    if (type(missing_column) == str):
        df_new = create_mnar_single(df, missing_column, p_missing, threshold, condition)
    elif (type(missing_column) == list):
        df_new = create_mnar_mult(df, missing_column, p_missing, threshold, condition)
    else:
        raise Exception('Name of the columns should be given as either str or list. Given format was {}'.format(
            type(missing_column)))
    return df_new

def test_mnar_single(df, missing_column, p_missing, threshold, condition):
    if condition == 'less':
        t = df[missing_column].isna()
        q = list(compress(range(len(t)), t)) #Which indices have NAs
        w = df[missing_column][q] > threshold #Which indices have a value greater than threshold value
        l = list(compress(range(len(w)), w)) #Indices of values greater than 5. Must be an empty set.
    
    elif condition == 'greater':
        t = df[missing_column].isna()
        q = list(compress(range(len(t)), t)) #Which indices have NAs
        w = df[missing_column][q] <= threshold #Which indices have a value less than or equal to threshold
        l = list(compress(range(len(w)), w)) #Indices of values greater than 5. Must be an empty set.
    
    else:
        raise Exception('Condition must be less or greater. Given condition was: {}'.format(condition))
    
    if len(l) == 0 and (df[missing_column].isna().sum() == round(p_missing * df.shape[0])):
        print("Missingness created for", missing_column, "succesfully!")
    else:
        print("Something is wrong.")
        
def test_mnar_mult(df, missing_column, p_missing, threshold, condition):
    for i in range(len(missing_column)):
        test_mnar_single(df, missing_column[i], p_missing, threshold[i], condition[i])
        
def test_mnar(df, missing_column, p_missing, threshold, condition):
    if (type(missing_column) == str):
        test_mnar_single(df, missing_column, p_missing, threshold, condition)
    elif (type(missing_column) == list):
        test_mnar_mult(df, missing_column, p_missing, threshold, condition)