#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 07:53:05 2020

@author: blaubaer (Ricky Helfgen)
"""
from scipy.stats import shapiro
#from scipy.stats import stats
import scipy as spy
from scipy.stats import median_test
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from outliers import smirnov_grubbs as grubbs
#import statistics as stats
from mft import isfloat, clear, session_write, print_table, save_CSV_new
from tabulate import tabulate
from scipy import stats
import numpy as np
import pandas as pd

F1 = '\U0001f522 ?'
F2 = '\U0001f521 ?' 

###############################################################################
###Statistical Tests
###############################################################################        


#######################################################################        
###test of normality
def normality_test(df):
    #clear()
    print('Test of normal distribution \n')
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column= input('Which value column do you want to verify: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
        
    y = df[list_columns_werte[int(value_column)]]
    y_val = list_columns_werte[int(value_column)]
    
    stat, p = shapiro(y)
    
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
        decision = 'Sample looks Gaussian (fail to reject H0)'
    else:
        print('Sample does not look Gaussian (reject H0)')
        decision = 'Sample does not look Gaussian (reject H0)'
    

    eintrag = 'Shapiro-Wilk - Test:' + '\nStatistics: ' + str(stat) + '\np-Value: ' + str(p) + '\ndecision: ' + decision
    
    plt.figure(figsize=(6,2))
    plt.subplot(211)
    spy.stats.probplot(y, dist="norm", plot=plt)
    
    plt.subplot(212)
    plt.text(0.1,0.5,eintrag, 
                     ha='left', va='center',
                     fontsize=12)
    plt.axis('off')
    plt.show() 
    
    ################################################################################
    ###Log-file
    fname = 'Test of normal distribution'
    fvalue = 'Value column: ' + y_val
    
    
    log = fname + '\n' + fvalue + '\n' + eintrag + '\n'
    session_write(log)



#######################################################################
###correlation test
def correl(df):
    #clear()
    print('Test of correlation \n')
    correlation_df = df.corr()
    
    
    count_column = len(correlation_df.columns)
    print('columns', count_column)
    if count_column > 13:
        print(correlation_df)
    else:
        print(tabulate(correlation_df, headers='keys', tablefmt='psql'))
    


    speichern_ja = input('Save the correlation table: y/n \n?')
    if speichern_ja.lower() =='y':
        csvfilename = input('Input only Filename ([filename].csv will save automaticly) \n?')
        fn = csvfilename + '.csv'
        correlation_df.to_csv(fn, sep=';', decimal=',', header =True)
    else:
        fn = 'none'    
    ################################################################################
    ###Log-file
    fname = 'Test of correlation'
    if count_column >13:
        view = 'Correlation table set'
    else:
        view = tabulate(correlation_df, headers='keys', tablefmt='psql')
    
    log = fname + '\n' + view + '\n'
    session_write(log)


###############################################################################
###correlation with only one column

def correlation_one_column(df):
    
    clear()
    
    print('Correlation Test one column \n')
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column= input('Which value column do you want to verify: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
        
    
    y_val = list_columns_werte[int(value_column)]
    
   
    
    correlation_df = df.corrwith(df[y_val])
    print(correlation_df)

    
    speichern_ja = input('Save the correlation table: y/n \n?')
    if speichern_ja.lower() =='y':
        csvfilename = input('Input only Filename ([filename].csv will save automaticly) \n?')
        fn = csvfilename + '.csv'
        correlation_df.to_csv(fn, sep=';', decimal=',', header =True)
    else:
        fn = 'none'    
    
################################################################################
    ###Log-file
    fname = 'Test of correlation'
    view = 'Column Name: ' + y_val
    log = fname + '\n' + view + '\n'
    session_write(log)



###############################################################################
###correlation with only one column

def correlation_one_column_whole_df(df):
    
    d = {'resp_Column': [], 'Correlation': [], 'Correl_with':[], 'Count datas': []}
    df2 = pd.DataFrame(data=d)
    clear()
    
    print('Delete Outlier whole Dataframe!')
    
    werte = df.select_dtypes(include=['float', 'float64'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column= input('Which value column do you want to choose: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    y_val = list_columns_werte[int(value_column)]
    
    
    rem_outl_yes = input('remove first outliers (quick and dirty method) y/n \n?')
    
    if rem_outl_yes == 'y':
        
        col_x = df.select_dtypes(include=['float', 'float64'])
        
        for col in col_x:
            print(col)
            q1 = df[col].quantile(0.25)
            print('Quantile0.25: ' , q1)
            q3 = df[col].quantile(0.75)
            print('Quantile0.75: ' , q3)
            if q1 == q3:
                print('no deviation in this column, no outlier')
            else:
                iqr = q3-q1 #Interquartile range
                fence_low  = q1-1.5*iqr
                fence_high = q3+1.5*iqr
                df_w_o = df.loc[(df[col] > fence_low) & (df[col] < fence_high)]
                print(df_w_o)
                countdf = len(df_w_o)
                print(countdf)
                #if countdf == 0:
                #    print('upsi, no data rest!')
                #if countdf < 10:
                #    input('only 10 data rest!')
                #input('press enter!')
                cor = df_w_o[col].corr(df_w_o[y_val])
                df2=df2.append({'resp_Column' : col , 'Correlation' : cor, 'Correl_with' : y_val, 'Count datas' : countdf} , ignore_index=True)
                print(df2)
        save_CSV_new(df2)
                
    else:
    
    
        correlation_df = df.corrwith(df[y_val])
        print(correlation_df)
        save_CSV_new(correlation_df)

     
    
      
    
################################################################################
    ###Log-file
    fname = 'Test of correlation'
    view = 'Column Name: ' + y_val
    log = fname + '\n' + view + '\n'
    session_write(log)







################################################################################
###remove outliers
#------------------------------------------------------------------------------
# accept a dataframe, remove outliers, return cleaned data in a new dataframe
# see http://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm
#------------------------------------------------------------------------------
def remove_outlier(df):
    
    werte = df.select_dtypes(include=['float', 'float64'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column= input('Which value column do you want to verify: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = df[list_columns_werte[int(value_column)]]
    y_val = list_columns_werte[int(value_column)]
    
    
    
    q1 = df[y_val].quantile(0.25)
    q3 = df[y_val].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df.loc[(df[y_val] > fence_low) & (df[y_val] < fence_high)]
    
    print(df_out)
    input('press enter!')
    save_CSV_new(df_out)

################################################################################
    ###Log-file
    fname = 'Delete Outliers into one column'
    fvalue = 'Value column: ' + y_val
    
    
    log = fname + '\n' + fvalue + '\n'
    session_write(log)





#######################################################################    
###Grubbs outlier test
def outliert(df):
    
    sns.set(color_codes=True)
    print('Test of Outliers \n')
    
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column= input('Which value column do you want to verify: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = df[list_columns_werte[int(value_column)]]
    y_val = list_columns_werte[int(value_column)]
    
    print('Value could be outlier:',grubbs.max_test_outliers(y, alpha=0.05))
    
       
    
    eintrag = 'Grubbs-Outlier Test' + '\nValue could be outlier:' + str(grubbs.max_test_outliers(y, alpha=0.05))
    
    plt.figure(figsize=(6,2))
    plt.subplot(211)
    sns.boxplot(x=y)
    plt.subplot(212)
    plt.text(0.1,0.5,eintrag, 
                     ha='left', va='center',
                     fontsize=12)
    plt.axis('off')
    plt.show()    
    
    input_del_outlier = ('Would yo like to delete the detected outliers y/n \n?')
    if input_del_outlier =='y':
        remove_outlier(df)
    
    
    ################################################################################
    ###Log-file
    fname = 'Test of Outliers'
    fvalue = 'Value column: ' + y_val
    
    
    log = fname + '\n' + fvalue + '\n' + eintrag + '\n'
    session_write(log)


###############################################################################
###delete outlier hole dataframe
def del_outlier(df):
    clear()
    
    print('Delete Outlier hole Dataframe!')
    
    werte = df.select_dtypes(include=['float', 'float64'])
    
    for col in werte:
        print(col)
        q1 = df[col].quantile(0.25)
        print('Quantile0.25: ' , q1)
        q3 = df[col].quantile(0.75)
        print('Quantile0.75: ' , q3)
        if q1 == q3:
            print('no deviation in this column, no outlier')
        else:
            iqr = q3-q1 #Interquartile range
            fence_low  = q1-1.5*iqr
            fence_high = q3+1.5*iqr
            df = df.loc[(df[col] > fence_low) & (df[col] < fence_high)]
            print(df)
            countdf = len(df)
            print(countdf)
            if countdf == 0:
                print('upsi, no data rest!')
            if countdf < 10:
                input('only 10 data rest!')
    print(df)
    input('press enter!')
    save_CSV_new(df)
################################################################################
    ###Log-file
    fname = 'Delete Outliers into the hole dataframe'
    fvalue = 'Value column: all value columns'
    
    
    log = fname + '\n' + fvalue + '\n' 
    session_write(log)


    
#######################################################################
###f-test
def f_test(df):
    clear()
    print('f-Test \n')
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column_a= input('a-value: \n(choose number) \n?')
        if value_column_a not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    while True:
        value_column_b= input('b-value: \n(choose number) \n?')
        if value_column_b not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    d1 = df[list_columns_werte[int(value_column_a)]]
    d1_val = list_columns_werte[int(value_column_a)]
    
    d2 = df[list_columns_werte[int(value_column_b)]]
    d2_val = list_columns_werte[int(value_column_b)]
    
    
    f, p = spy.stats.f_oneway(d1, d2)
    
    
    print('f-Test:')
    
    print('F-Value:' ,f)
    print('p-value:' ,p)
    
    
    
    
    alpha = 0.05
    if p > alpha:
        print('Variances should be equal (fail to reject H0)')
        erg = 'Variances should be equal (fail to reject H0)'
    else:
        print('Variances should not be equal (reject H0)')    
        erg = 'Variances should not be equal (reject H0)'
    
    eintrag = 'F-Value: ' + str(f) + ' p-Value: ' + str(p) + '\n' + erg 
    
    ################################################################################
    ###Log-file
    fname = 'f-Test'
    fvalue = 'Column 1: ' + d1_val + ' Column 2: ' + d2_val 
    
    
    log = fname + '\n' + fvalue + '\n' + eintrag
    session_write(log)


#######################################################################    
###one single t-test
def ttest_o_s(df, alpha=0.05, alternative='greater'):
    clear()
    print('One sample t-Test \n')
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column= input('Which value column do you want to verify: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    while True:
        target_value = input('Input taget mean-value \n(choose point-comma \n?')
    
        if not isfloat(target_value):
            print("Target mean value is not a number with point-comma, please try again")
        else:
            break
    
    
    y = df[list_columns_werte[int(value_column)]]
    y_val = list_columns_werte[int(value_column)]
    try:
        t, p = spy.stats.ttest_1samp(y, float(target_value))
    
    
        print('One sample t-Test:')
        print ('t-Value:',t)
        print ('p-Value:',p)
    
        alpha = 0.05
        if p > alpha:
            print('Means should not be different (fail to reject H0)')
            erg = 'Means should not be different (fail to reject H0)'
        
        else:
            
            print('Means should be different (reject H0)')
            erg = 'Means should be different (reject H0)'
    except Exception as exception:
                print('Wrong input (choose point-comma), please try again!')
    
    
    eintrag = 't-Value: ' + str(t) + ' p-Value: ' + str(p) + '\n' + erg 
    
    ################################################################################
    ###Log-file
    fname = 'One sample t-Test'
    fvalue = 'Value Column: ' + y_val + ' Target-Value: ' + str(target_value)  
    
    
    log = fname + '\n' + fvalue + '\n' + eintrag
    session_write(log)
    
    
#######################################################################    
###two sided t-test
def ttest_t_s(df):
    #clear()
    print('two sample t-Test \n')
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column_a= input('a-value: \n(choose number) \n?')
        if value_column_a not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    while True:
        value_column_b= input('b-value: \n(choose number) \n?')
        if value_column_b not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
    a = df[list_columns_werte[int(value_column_a)]]
    a_val = list_columns_werte[int(value_column_a)]
    
    b = df[list_columns_werte[int(value_column_b)]]
    b_val = list_columns_werte[int(value_column_b)]
    
    
    try:
        t, p = spy.stats.ttest_rel(a,b)
    
    
        print('Two sample t-Test:')
        print ('t-Value:',t)
        print ('p-Value:',p)
    
        alpha = 0.05
        if p > alpha:
            print('Means should not be different (fail to reject H0)')
            erg = 'Means should not be different (fail to reject H0)'
        else:
            print('Means should be different (reject H0)')
            erg = 'Means should be different (reject H0)'
    except Exception as exception:
                print('Wrong input (choose point-comma), please try again!')
                
    eintrag = 't-Value: ' + str(t) + ' p-Value: ' + str(p) + '\n' + erg
    
    ################################################################################
    ###Log-file
    fname = 'Two sample t-Test'
    fvalue = 'Value Column 1: ' + a_val + 'Value Column 2: ' + b_val 
    
    
    log = fname + '\n' + fvalue + '\n' + eintrag
    session_write(log)
    
    
    
    
#######################################################################                
###indipendent t-test
def ttest_i(df):
    #clear()
    print('Indipendent t-Test \n')
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column_a= input('a-value: \n(choose number) \n?')
        if value_column_a not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    while True:
        value_column_b= input('b-value: \n(choose number) \n?')
        if value_column_b not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    a = df[list_columns_werte[int(value_column_a)]]
    a_val = list_columns_werte[int(value_column_a)]
    b = df[list_columns_werte[int(value_column_b)]]
    b_val = list_columns_werte[int(value_column_b)]
    
    
    try:
        t, p = spy.stats.ttest_ind(a,b, equal_var = False)
    
    
        print('Indipendent sample t-Test (for the means of two independent samples of scores):')
        print ('t-Value:',t)
        print ('p-Value:',p)
    
        alpha = 0.05
        
        if p > alpha:
            print('Means should not be different (fail to reject H0)')
            erg = 'Means should not be different (fail to reject H0)'
        else:
            print('Means should be different (reject H0)')
            erg = 'Means should be different (reject H0)'
    except Exception as exception:
                print('Wrong input, please try again!')

    
    eintrag = 't-Value: ' + str(t) + ' p-Value: ' + str(p) + '\n' + erg
    
    ################################################################################
    ###Log-file
    fname = 'Indipendent sample t-Test'
    fvalue = 'Value Column 1: ' + a_val + 'Value Column 2: ' + b_val 
    
    
    log = fname + '\n' + fvalue + '\n' + eintrag
    session_write(log)


#######################################################################
###median test
def mediantest(df):
    print('Median Test \n')
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column_a= input('a-value: \n(choose number) \n?')
        if value_column_a not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    while True:
        value_column_b= input('b-value: \n(choose number) \n?')
        if value_column_b not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
    a = df[list_columns_werte[int(value_column_a)]]
    a_val = list_columns_werte[int(value_column_a)]
    b = df[list_columns_werte[int(value_column_b)]]
    b_val = list_columns_werte[int(value_column_b)]
    
    med1=a.median()
    med2=b.median()
    
    diff = abs(med1-med2)
    
    print('Median Group a: ', med1)
    print('Median Group b: ', med2)
    print('Differences :', diff)
    
    
    
    try:
        
        stat, p, med, tbl = median_test(a, b)
    
    
        print('Median-Test:')
        print ('stat-Value:',stat)
        print ('p-Value:',p)
    
        alpha = 0.05
        if p > alpha:
            print('Medians should not be different (fail to reject H0)')
            erg = 'Medians should not be different (fail to reject H0)'
        else:
            print('Medians should be different (reject H0)')
            erg = 'Medians should be different (reject H0)'
    except Exception as exception:
                print('Wrong input (choose point-comma), please try again!')
                

    eintrag = 'median column 1: ' + str(med1) + ' median column 2: ' + str(med2) + '\n' + 'Difference: ' + str(diff)
    eintrag2 = 'Stat-Value: ' + str(stat) + '\n' + 'p-Value: ' + str(p) + '\n' + erg
    
    ################################################################################
    ###Log-file
    fname = 'Median-Test'
    fvalue = 'Value Column 1: ' + a_val + 'Value Column 2: ' + b_val 
    
    
    log = fname + '\n' + fvalue + '\n' + eintrag + '\n' + eintrag2
    session_write(log)


#######################################################################    
###One way ANOVA    
def anova_o_w (df):
    clear()
    print('One way ANOVA \n')
    kategorie=df.select_dtypes(include=['object', 'int'])
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number =[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    while True:
        value_column= input('Which value column do you want to see: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number=[]
    i=1
    for i in range(anz_col_kategorie):
        list_columns_kategorie.append(kategorie.columns[i])
        list_number.append(str(i))
        print(i, kategorie.columns[i])
        i+=1
    
    while True:
        groupby_column = input('Group by column: \n(choose number) \n?')
        if groupby_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_kategorie[int(groupby_column)]
    
    mod = ols(y + '~' + x,
                data=df).fit()
                
    aov_table = sm.stats.anova_lm(mod, typ=2)
    print('one way ANOVA Result:' )
    
    
    print_table(aov_table)
    view1 = tabulate(aov_table, headers='keys', tablefmt='psql')
    
    
    ################################################################################
    ###Log-file
    fname = 'One way ANOVA'
    fvalue = 'Value Column: ' + y + 'Category Column: ' + x 
    
    
    log = fname + '\n' + fvalue + '\n' + view1
    session_write(log)

    
    
    
    
#######################################################################    
###Two way ANOVA    
def anova_t_w(df):
    clear()
    print('Two way ANOVA \n')
    kategorie=df.select_dtypes(exclude=['float'])
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number=[]
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    
    while True:
        value_column= input('Which value column do you want to compare: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number=[]
    i=1
    for i in range(anz_col_kategorie):
        list_columns_kategorie.append(kategorie.columns[i])
        list_number.append(str(i))
        print(i, kategorie.columns[i])
        i+=1
    
    
    
    while True:
        faktor1 = input('Factor1: \n(choose number) \n?')
        if faktor1 not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    while True:
        faktor2 = input('Factor2: \n(choose number) \n?')
        if faktor2 not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    
    y = list_columns_werte[int(value_column)]
    a = list_columns_kategorie[int(faktor1)]
    b = list_columns_kategorie[int(faktor2)]
    
    mod = ols(y + '~C(' + a + ')*C(' + b +')',
                data=df).fit()

    # Seeing if the overall model is significant
    print(f"Overall mod F({mod.df_model: .0f},{mod.df_resid: .0f}) = {mod.fvalue: .3f}, p = {mod.f_pvalue: .4f}")    
    
    mod.summary()
        
    aov_table = sm.stats.anova_lm(mod, typ=2)
    print('two way ANOVA Result:' )
    #print (aov_table)
    
    print_table(aov_table)
    view1 = tabulate(aov_table, headers='keys', tablefmt='psql')
    


    ################################################################################
    ###Log-file
    fname = 'Two way ANOVA'
    fvalue = 'Value Column: ' + y + 'Category Column1: ' + a + 'Category Column2: ' + b 
    
    
    log = fname + '\n' + fvalue + '\n' + view1
    session_write(log)
    