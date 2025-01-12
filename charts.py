#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 11:55:01 2020

@author: blaubaer (Ricky Helfgen)
"""
import seaborn as sns
import matplotlib.pyplot as plt
import scipy as spy
from scipy.stats import shapiro
from mft import isfloat, clear, truncate, moving_average, isinteger, session_write
import pandas as pd
#from mpl_toolkits import mplot3d
#from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting 
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 


    
##################################################################################
#graphical analyze
##################################################################################

#######################################################################
####bar charts
### groupby barchart

def groupby_balkendiagramm(df):
    clear()
    print('Bar-chart with Group\n')
    anz_col = len(df.columns)
        
    list_columns = []
    list_number=[]
    i=1
    for i in range(anz_col):
        list_columns.append(df.columns[i])
        list_number.append(str(i))
        print(i, df.columns[i])
        i+=1
    
    while True:
        nummer_spalte= input('Which column do you want to see: \n(choose number) \n?')
        if nummer_spalte not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    while True:
        groupby_spalte = input('Group by column: \n(choose number) \n?')
        if groupby_spalte not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    y = list_columns[int(nummer_spalte)]
    x = list_columns[int(groupby_spalte)]
    
    ###########################################################################
    ###session-datei
    
    fname = 'Bar-chart with Group'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n'
    session_write(log)


    ###########################################################################
    ###plot
    
    df.groupby([list_columns[int(nummer_spalte)],list_columns[int(groupby_spalte)]]).size().unstack().plot(kind='bar',stacked=True)
    label_chart = (list_columns[int(nummer_spalte)] + ' grouped by count ' + list_columns[int(groupby_spalte)])
    plt.title(label_chart, fontdict=None, loc='center', pad=None)
    
    
    
    
    plt.show()
    
    #df.groupby('state')['name'].nunique().plot(kind='bar')
    #plt.show()

#######################################################################
### barcharts
def balkendiagramm(df):
    clear()
    print('Bar-Chart - count entries one column \n')
    anz_col = len(df.columns)
        
    list_columns = []
    list_number=[]
    i=1
    for i in range(anz_col):
        list_columns.append(df.columns[i])
        list_number.append(str(i))
        print(i, df.columns[i])
        i+=1
        
    while True:
        nummer_spalte= input('Which column do you want to see: \n(choose number) \n?')
        if nummer_spalte not in list_number:
            print('wrong input, try again!')
        else:
            break    
    
    y = list_columns[int(nummer_spalte)]
    
    ###########################################################################
    ###session-datei
    
    fname = 'Bar-chart with Group'
    fvalue = 'Value: ' + y
    #fbygroup = 'Group by: ' + x
    
    
    log = fname + '\n' + fvalue + '\n'
    session_write(log)
    
    
    
    ax = df[list_columns[int(nummer_spalte)]].value_counts().plot(kind='bar',
                                    figsize=(14,8),
                                    title=list_columns[int(nummer_spalte)], color='blue')
    ax.set_xlabel(list_columns[int(nummer_spalte)])
    ax.set_ylabel("Frequency")
    plt.show()


#######################################################################        
###pie charts
def kuchendiagramm(df):
    clear()
    print('Pie-Chart \n')
    anz_col = len(df.columns)
        
    list_columns = []
    list_number = []
    i=1
    for i in range(anz_col):
        list_columns.append(df.columns[i])
        list_number.append(str(i))
        print(i, df.columns[i])
        i+=1
    
    while True:
        nummer_spalte= input('Which column do you want to see: \n(choose number) \n?')
        if nummer_spalte not in list_number:
            print('wrong input, try again!')
        else:
            break    
    
    y = list_columns[int(nummer_spalte)]
    
    ###########################################################################
    ###session-datei
    
    fname = 'Pi-chart with Group'
    fvalue = 'Value: ' + y
    
    
    
    log = fname + '\n' + fvalue + '\n'
    session_write(log)
    
    
    ###########################################################################    
    # Plot
    ax = df[list_columns[int(nummer_spalte)]].value_counts().plot(kind='pie',
                                    figsize=(14,8),
                                    title=list_columns[int(nummer_spalte)], autopct='%1.1f%%')
    #ax.set_xlabel(list_columns[int(nummer_spalte)])
    ax.set_ylabel("Frequency")
    
    
    plt.show()

#######################################################################
###line-chart
def liniendiagramm(df):
    clear()
    print('Line-Chart \n')
    kategorie=df.select_dtypes(include=['object', 'datetime', 'int'])
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number = []
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    
    while True:
        value_column= input('Which value column do you want to see: \n(choose number)\n')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number = []
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
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        df.plot(x, y)
        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            df.plot(x, y)
            
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.xticks(rotation=45)
            
            plt.show()
            
        elif ut=='none':
            
            df.plot(x, y)
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            df.plot(x, y)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Line-Chart'
    fvalue = 'Value: ' + y
    fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)

    
    

###line-chart with dots
def liniendiagramm_w_dot(df):
    clear()
    print('Line-Chart with dot \n')
    kategorie=df.select_dtypes(include=['object', 'datetime', 'int'])
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number = []
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    
    while True:
        value_column= input('Which value column do you want to see: \n(choose number)\n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number = []
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
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        df.plot(x, y, style='-o')
        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            df.plot(x, y, style='-o')
            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            df.plot(x, y, style='-o')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            df.plot(x, y, style='-o')
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    ###########################################################################
    ###session-datei
    
    fname = 'Line-Chart with dots'
    fvalue = 'Value: ' + y
    fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
    
    
    
###line-chart with dots
def liniendiagramm_w_dot_cumsum(df):
    clear()
    print('Line-Chart with dot and cumsum\n')
    kategorie=df.select_dtypes(include=['object', 'datetime', 'int'])
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number = []
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    
    while True:
        value_column= input('Which value column do you want to see: \n(choose number)\n')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number = []
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
    
    while True:
        nsize = input('Size of cumsum: \n')
        if not isinteger(nsize):
            print('input is not an integer, please try again')
        else:
            break
        
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_kategorie[int(groupby_column)]
    df2 = pd.DataFrame()
    df2['cumsum'] = moving_average(df[y], w=int(nsize))
    df2['number'] = range(1, len(df2) + 1)
    titlecumsum = 'cumsum-chart for '+ y + '; n=' + nsize
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        df.plot(x, y, style='-o')
        df2.plot('number','cumsum',  title=titlecumsum )
        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
        
        if lt =='none':
              
            df.plot(x, y, style='-o')
            
            plt.axhline(y=ut,linewidth=2, color='red')
            df2.plot('number','cumsum',  title=titlecumsum )
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            df.plot(x, y, style='-o')
            plt.axhline(y=lt,linewidth=2, color='red')
            df2.plot('number','cumsum',  title=titlecumsum )
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
            
            df.plot(x, y, style='-o')
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            df2.plot('number','cumsum', title=titlecumsum )
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
                        
            plt.xticks(rotation=45)
            plt.show()
    
    ###########################################################################
    ###session-datei
    
    fname = 'Line-Chart with dot and cumsum'
    fvalue = 'Value: ' + y
    fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
    
def line_diagram_menu(df):
    
    clear()
    print('Line-Chart-Menue \n')
    ld_menu = input('Which kind of line diagram: \n1: line with dots \n2: line without dots \n3: line with dot and cumsum \n?')
    
    if ld_menu == '1':
        liniendiagramm_w_dot(df)
    elif ld_menu == '2':
        liniendiagramm(df)
    elif ld_menu =='3':
        liniendiagramm_w_dot_cumsum(df)
    else:
        print('wrong input (choose number), try again!')


#######################################################################
###line-chart
def confidencelinechart(df):
    
    #df = sns.load_dataset(df)
    
    clear()
    print('Confidence Level Chart \n')
    kategorie=df.select_dtypes(include=['object', 'datetime', 'int'])
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number = []
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    
    while True:
        value_column= input('Which value column do you want to see: \n(choose number)\n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number = []
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
    
    sns.relplot(x=x, y=y, kind="line", ci="sd", data=df)
    
    
    plt.show()

    ###########################################################################
    ###session-datei
    
    fname = 'Confidence Linechart'
    fvalue = 'Value: ' + y
    fbygroup = 'X-Achse: ' + x
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' 
    session_write(log)


#######################################################################
###boxplots and violinplots

#######################################################################
###single boxplot    
def boxplot(df):
    clear()
    print('Simple Boxplot \n')
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
    
    
    y = list_columns_werte[int(value_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        df.boxplot(column=y, widths=0.5)
        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            df.boxplot(column=y, widths=0.5)
            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            df.boxplot(column=y, widths=0.5)
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.show()
        
        
        else:
        
            df.boxplot(column=y, widths=0.5)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Boxplot'
    fvalue = 'Value: ' + y
    #fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + tol + '\n'
    session_write(log)
    
    
#######################################################################
###single boxplot    
def boxplot_w_dot(df):
    clear()
    print('Simple Boxplot \n')
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
    
    
    y = list_columns_werte[int(value_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.boxplot(y=y, data=df,
            whis=[0, 100], width=.6, palette="vlag")
        sns.stripplot(y=y, data=df,
              size=4, color=".3", linewidth=0)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            
            sns.boxplot(y=y, data=df,
            whis=[0, 100], width=.6, palette="vlag")
            sns.stripplot(y=y, data=df,
              size=4, color=".3", linewidth=0)
            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            sns.boxplot(y=y, data=df,
            whis=[0, 100], width=.6, palette="vlag")
            sns.stripplot(y=y, data=df,
              size=4, color=".3", linewidth=0)
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.show()
        
        
        else:
        
            sns.boxplot(y=y, data=df,
            whis=[0, 100], width=.6, palette="vlag")
            sns.stripplot(y=y, data=df,
              size=4, color=".3", linewidth=0)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Boxplot with observations'
    fvalue = 'Value: ' + y
    #fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + tol + '\n'
    session_write(log)
    
    
    
    
    
    
    
    

#######################################################################
###boxplot with group
def boxplot_groupby(df):
    clear()
    print('Boxplot with one Group \n')
    kategorie=df.select_dtypes(include=['object','int'])
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
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        df.boxplot(by=x, column=y)
        plt.xticks(rotation=45)    
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            df.boxplot(by=x, column=y)
            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            df.boxplot(by=x, column=y)
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            df.boxplot(by=x, column=y)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Boxplot by Group'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
#######################################################################
###boxplot with group
def boxplot_groupby_w_o(df):
    clear()
    print('Boxplot with one Group \n')
    kategorie=df.select_dtypes(include=['object','int'])
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
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.boxplot(x=x, y=y, data=df,
            whis=[0, 100], width=.6, palette="vlag")
        sns.stripplot(x=x, y=y, data=df,
              size=4, color=".3", linewidth=0)
        
        plt.xticks(rotation=45)    
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            sns.boxplot(x=x, y=y, data=df,
            whis=[0, 100], width=.6, palette="vlag")
            sns.stripplot(x=x, y=y, data=df,
              size=4, color=".3", linewidth=0)
            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            sns.boxplot(x=x, y=y, data=df,
            whis=[0, 100], width=.6, palette="vlag")
            sns.stripplot(x=x, y=y, data=df,
              size=4, color=".3", linewidth=0)
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            sns.boxplot(x=x, y=y, data=df,
            whis=[0, 100], width=.6, palette="vlag")
            sns.stripplot(x=x, y=y, data=df,
              size=4, color=".3", linewidth=0)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Boxplot by Group with Observations'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)


######################################################################
### Boxplot by 2 groups
    
def boxplot2f(df):
    
    clear()
    print('Boxplot with two Groups \n')
    sns.set(style="whitegrid")
    
    category=df.select_dtypes(exclude=['float'])
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
    anz_col_category = len(category.columns)
        
    list_columns_category = []
    list_number=[]
    i=1
    for i in range(anz_col_category):
        list_columns_category.append(category.columns[i])
        list_number.append(str(i))
        print(i, category.columns[i])
        i+=1
    
    while True:
        groupby1_column = input('Group1 by column: \n(choose number) \n?')
        if groupby1_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    while True:
        groupby2_column = input('Group2 by column \n(choose number) \n?')
        if groupby2_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_category[int(groupby1_column)]
    z = list_columns_category[int(groupby2_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.boxplot(x=x, y=y, hue=z, data=df, palette="Set3")
        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            sns.boxplot(x=x, y=y, hue=z, data=df, palette="Set3")
            
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.xticks(rotation=45)
            
            plt.show()
            
        elif ut=='none':
            
            sns.boxplot(x=x, y=y, hue=z, data=df, palette="Set3")
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            sns.boxplot(x=x, y=y, hue=z, data=df, palette="Set3")
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    ###########################################################################
    ###session-datei
    
    fname = 'Boxplot by 2 Factors'
    fvalue = 'Value: ' + y
    fbygroup = 'Factor1: ' + x + '; ' + 'Factor2: ' + z
    
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
    
    
    
   
#######################################################################    
###single violin plot
def violin(df):
    clear()
    print('Simple Violin Plot \n')
    sns.set(style="whitegrid")
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
        value_column= input('Which value column do you want to see: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
    
    y = list_columns_werte[int(value_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.violinplot(x=df[y])
        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            sns.violinplot(x=df[y])
            
            plt.axvline(x=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            sns.violinplot(x=df[y])
            plt.axvline(x=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            sns.violinplot(x=df[y])
            plt.axvline(x=ut,linewidth=2, color='red')
            plt.axvline(x=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Violinplot'
    fvalue = 'Value: ' + y
    #fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + tol + '\n'
    session_write(log)



#######################################################################
###violin plot with group
def violin_groupby(df):
    clear()
    print('Violin Plot with one Group \n')
    sns.set(style="whitegrid")
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
        value_column= input('Which value column do you want to see: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number = []
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
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.violinplot(x=x, y=y, data=df)
        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            sns.violinplot(x=x, y=y, data=df)
            
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            sns.violinplot(x=x, y=y, data=df)
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            sns.violinplot(x=x, y=y, data=df)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    ###########################################################################
    ###session-datei
    
    fname = 'Violinplot by Group'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)

    
    
#######################################################################
###violin Plot by 2 groups
def violin2f(df):
    clear()
    print('Violin Plot with two Groups \n')
    sns.set(style="whitegrid")
    
    category=df.select_dtypes(exclude=['float'])
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
    anz_col_category = len(category.columns)
        
    list_columns_category = []
    list_number=[]
    i=1
    for i in range(anz_col_category):
        list_columns_category.append(category.columns[i])
        list_number.append(str(i))
        print(i, category.columns[i])
        i+=1
    
    while True:
        groupby1_column = input('Group1 by column: \n(choose number) \n?')
        if groupby1_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    while True:
        groupby2_column = input('Group2 by column \n(choose number) \n?')
        if groupby2_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_category[int(groupby1_column)]
    z = list_columns_category[int(groupby2_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.violinplot(x=x, y=y, hue=z, data=df, palette="Set3")
        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            sns.violinplot(x=x, y=y, hue=z, data=df, palette="Set3")
            
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.xticks(rotation=45)
            
            plt.show()
            
        elif ut=='none':
            
            sns.violinplot(x=x, y=y, hue=z, data=df, palette="Set3")
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            sns.violinplot(x=x, y=y, hue=z, data=df, palette="Set3")
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Violinplot by 2 Factors'
    fvalue = 'Value: ' + y
    fbygroup = 'Factor1: ' + x + '; ' + 'Factor2: ' + z
    
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
    
    

######################################################################
###single swarm plot
def single_swarmplot(df):
    clear()
    print('Simple Swarm Plot \n' )
    sns.set(style="whitegrid")
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
        value_column= input('Which value column do you want to see: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
    
    y = list_columns_werte[int(value_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.swarmplot(x=df[y])
        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            sns.swarmplot(x=df[y])
            
            plt.axvline(x=ut,linewidth=2, color='red')
            plt.xticks(rotation=45)
            
            plt.show()
            
        elif ut=='none':
            
            sns.swarmplot(x=df[y])
            plt.axvline(x=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            sns.swarmplot(x=df[y])
            plt.axvline(x=ut,linewidth=2, color='red')
            plt.axvline(x=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Swarmplot'
    fvalue = 'Value: ' + y
    #fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + tol + '\n'
    session_write(log)

    
    
    
    
    
    
#######################################################################
###swarmplot with group
def swarmplot1f(df):
    clear()
    print('Swarm Plot with one Group \n')
    sns.set(style="whitegrid", palette="muted")

    kategorie=df.select_dtypes(exclude=['float'])
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
    
    y = df[list_columns_werte[int(value_column)]]
    y_val = list_columns_werte[int(value_column)]
    x = df[list_columns_kategorie[int(groupby_column)]]
    x_val = list_columns_kategorie[int(groupby_column)]
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        # Draw a categorical scatterplot to show each observation
        sns.swarmplot(x=x, y=y, data=df)
        plt.xticks(rotation=45)
        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            # Draw a categorical scatterplot to show each observation
            sns.swarmplot(x=x, y=y, data=df)

            plt.axhline(y=ut,linewidth=2, color='red')
            plt.xticks(rotation=45)
            
            plt.show()
            
        elif ut=='none':
            
            # Draw a categorical scatterplot to show each observation
            sns.swarmplot(x=x, y=y, data=df)

            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            # Draw a categorical scatterplot to show each observation
            sns.swarmplot(x=x, y=y, data=df)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Swarmplot by Group'
    fvalue = 'Value: ' + y_val
    fbygroup = 'Group by: ' + x_val
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)

    
    
######################################################################
###swarmplot two factors
def swarmplot2f(df):
    clear()
    print('Swarm Plot with two Groups \n')
    sns.set(style="whitegrid")
    
    category=df.select_dtypes(exclude=['float'])
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
    anz_col_category = len(category.columns)
        
    list_columns_category = []
    list_number=[]
    i=1
    for i in range(anz_col_category):
        list_columns_category.append(category.columns[i])
        list_number.append(str(i))
        print(i, category.columns[i])
        i+=1
    
    while True:
        groupby1_column = input('Group1 by column: \n(choose number) \n?')
        if groupby1_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    while True:
        groupby2_column = input('Group2 by column \n(choose number) \n?')
        if groupby2_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_category[int(groupby1_column)]
    z = list_columns_category[int(groupby2_column)]
    

    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        # Draw a categorical scatterplot to show each observation
        sns.swarmplot(x=x, y=y, hue=z, data=df)

        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            # Draw a categorical scatterplot to show each observation
            sns.swarmplot(x=x, y=y, hue=z, data=df)

            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            # Draw a categorical scatterplot to show each observation
            sns.swarmplot(x=x, y=y, hue=z, data=df)

            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            # Draw a categorical scatterplot to show each observation
            sns.swarmplot(x=x, y=y, hue=z, data=df)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()


    ###########################################################################
    ###session-datei
    
    fname = 'Swarmplot by 2 Factors'
    fvalue = 'Value: ' + y
    fbygroup = 'Factor1: ' + x + '; ' + 'Factor2: ' + z
    
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    

######################################################################
###single stripplot
def single_stripplot(df):
    clear()
    print('Single Strip Plot \n')
    sns.set(style="whitegrid")
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
        value_column= input('Which value column do you want to see: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
    
    y = list_columns_werte[int(value_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        # Draw a categorical scatterplot to show each observation
        sns.stripplot(x=df[y])

        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=df[y])

            
            plt.axvline(x=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=df[y])

            plt.axvline(x=lt,linewidth=2, color='red')
            plt.show()
        
        
        else:
        
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=df[y])
            plt.axvline(x=ut,linewidth=2, color='red')
            plt.axvline(x=lt,linewidth=2, color='red')
            
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Stripplot'
    fvalue = 'Value: ' + y
    #fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + tol + '\n'
    session_write(log)

    
    
    
    #sns.stripplot(x=df[y])
    #plt.show()
    
#######################################################################
###stripplot with group
def stripplot1f(df):
    clear()
    print('Strip Plot with one Group \n')
    sns.set(style="whitegrid", palette="muted")

    kategorie=df.select_dtypes(exclude=['float'])
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
    
    y = df[list_columns_werte[int(value_column)]]
    y_val = list_columns_werte[int(value_column)]
    x = df[list_columns_kategorie[int(groupby_column)]]
    x_val = list_columns_kategorie[int(groupby_column)]
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        # Draw a categorical scatterplot to show each observation
        sns.stripplot(x=x, y=y, data=df)

        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=x, y=y, data=df)

            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=x, y=y, data=df)

            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=x, y=y, data=df)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Stripplot by Group'
    fvalue = 'Value: ' + y_val
    fbygroup = 'Group by: ' + x_val
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
######################################################################
###stripplot two factors
def stripplot2f(df):
    clear()
    print('Strip Plot with two Groups \n')
    sns.set(style="whitegrid")
    
    category=df.select_dtypes(exclude=['float'])
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
    anz_col_category = len(category.columns)
        
    list_columns_category = []
    list_number=[]
    i=1
    for i in range(anz_col_category):
        list_columns_category.append(category.columns[i])
        list_number.append(str(i))
        print(i, category.columns[i])
        i+=1
    
    while True:
        groupby1_column = input('Group1 by column: \n(choose number) \n?')
        if groupby1_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    while True:
        groupby2_column = input('Group2 by column \n(choose number) \n?')
        if groupby2_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_category[int(groupby1_column)]
    z = list_columns_category[int(groupby2_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        # Draw a categorical scatterplot to show each observation
        sns.stripplot(x=x, y=y, hue=z, data=df)

        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=x, y=y, hue=z, data=df)

            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=x, y=y, hue=z, data=df)

            plt.axhline(y=lt,linewidth=2, color='red')
            plt.show()
        
        
        else:
        
            # Draw a categorical scatterplot to show each observation
            sns.stripplot(x=x, y=y, hue=z, data=df)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Stripplot by 2 Factors'
    fvalue = 'Value: ' + y
    fbygroup = 'Factor1: ' + x + '; ' + 'Factor2: ' + z
    
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
    
    
    
#######################################################################
###stripplot with group
def pointplot1f(df):
    clear()
    
    print('Point Plot by one Group \n')
    sns.set(style="darkgrid")

    kategorie=df.select_dtypes(exclude=['float'])
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
    
    y = df[list_columns_werte[int(value_column)]]
    
    y_val = list_columns_werte[int(value_column)]
    x = df[list_columns_kategorie[int(groupby_column)]]
    x_val = list_columns_kategorie[int(groupby_column)]
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        # Draw a categorical scatterplot to show each observation
        sns.pointplot(x=x, y=y, data=df)

        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            # Draw a categorical scatterplot to show each observation
            sns.pointplot(x=x, y=y, data=df)

            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            # Draw a categorical scatterplot to show each observation
            sns.pointplot(x=x, y=y, data=df)

            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            # Draw a categorical scatterplot to show each observation
            sns.pointplot(x=x, y=y, data=df)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    ###########################################################################
    ###session-datei
    
    fname = 'Pointplot by Group'
    fvalue = 'Value: ' + y_val
    fbygroup = 'Group by: ' + x_val
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
    
    
        
######################################################################
###stripplot two factors
def pointplot2f(df):
    clear()
    
    print('Point Plot by two Groups \n')
    sns.set(style="darkgrid")
    
    category=df.select_dtypes(exclude=['float'])
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
    anz_col_category = len(category.columns)
        
    list_columns_category = []
    list_number=[]
    i=1
    for i in range(anz_col_category):
        list_columns_category.append(category.columns[i])
        list_number.append(str(i))
        print(i, category.columns[i])
        i+=1
    
    while True:
        groupby1_column = input('Group1 by column: \n(choose number) \n?')
        if groupby1_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    while True:
        groupby2_column = input('Group2 by column \n(choose number) \n?')
        if groupby2_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_category[int(groupby1_column)]
    z = list_columns_category[int(groupby2_column)]
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        # Draw a categorical scatterplot to show each observation
        sns.pointplot(x=x, y=y, hue=z, data=df)

        plt.xticks(rotation=45)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            # Draw a categorical scatterplot to show each observation
            sns.pointplot(x=x, y=y, hue=z, data=df)

            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=45)
            plt.show()
            
        elif ut=='none':
            
            # Draw a categorical scatterplot to show each observation
            sns.pointplot(x=x, y=y, hue=z, data=df)

            plt.axhline(y=lt,linewidth=2, color='red')
            
            plt.xticks(rotation=45)
            plt.show()
        
        
        else:
        
            # Draw a categorical scatterplot to show each observation
            sns.pointplot(x=x, y=y, hue=z, data=df)
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=45)
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Pointplot by 2 Factors'
    fvalue = 'Value: ' + y
    fbygroup = 'Factor1: ' + x + '; ' + 'Factor2: ' + z
    
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)



    
    
################################################################################
###visual distribution and values
###histogram
def histogram(df):
    clear()
    
    print('Histogram \n')
    sns.set(color_codes=True)

        
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number = []
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
    
    
    
    
    y = df[list_columns_werte[int(value_column)]]
    y_val = list_columns_werte[int(value_column)]
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.displot(y, kde=True);

        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            sns.displot(y, kde=True);

            
            plt.axvline(x=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            sns.displot(y, kde=True);

            plt.axvline(x=lt,linewidth=2, color='red')
            plt.show()
        
        
        else:
        
            
            sns.displot(y, kde=True);
            plt.axvline(x=ut,linewidth=2, color='red')
            plt.axvline(x=lt,linewidth=2, color='red')
            
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Histogram'
    fvalue = 'Value: ' + y_val
    #fbygroup = 'X-Achse: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + tol + '\n'
    session_write(log)


###distriplot with group
def distriplot1f(df):
    clear()
    print('Distributions-Plot \n')
    sns.set(style="darkgrid")
    kategorie=df.select_dtypes(exclude=['float'])
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
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.displot(df, x=y, hue =x, kind='kde', fill=True)

        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            
            sns.displot(df, x=y, hue=x, kind='kde', fill=True)
            
            plt.axvline(x=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            
            sns.displot(df, x=y,  hue=x, kind='kde', fill=True)

            plt.axvline(x=lt,linewidth=2, color='red')
            plt.show()
        
        
        else:
        
            
            sns.displot(df, x=y, hue = x, kind='kde', fill=True)
            plt.axvline(x=ut,linewidth=2, color='red')
            plt.axvline(x=lt,linewidth=2, color='red')
            
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Distribution Plot by one factor'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    
    
    
    
def histogram1f(df):
    clear()
    print('Histogram by one factor \n')
    sns.set(style="darkgrid")
    kategorie=df.select_dtypes(exclude=['float'])
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
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        sns.displot(df, x=y, hue =x, kind='hist', fill=True)

        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            
            sns.displot(df, x=y, hue=x, kind='hist', fill=True)
            
            plt.axvline(x=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            
            sns.displot(df, x=y,  hue=x, kind='hist', fill=True)

            plt.axvline(x=lt,linewidth=2, color='red')
            plt.show()
        
        
        else:
        
            
            sns.displot(df, x=y, hue = x, kind='hist', fill=True)
            plt.axvline(x=ut,linewidth=2, color='red')
            plt.axvline(x=lt,linewidth=2, color='red')
            
            plt.show()
################################################################################
###Log-file
    fname = 'Histogram by one factor'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)
    

#######################################################################    
###qq-plot
def qq_plot(df):
    clear()
    print('Q-Q-Plot \n')
    werte = df.select_dtypes(exclude=['object'])
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number = []
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
        
    y = df[list_columns_werte[int(value_column)]]
    
    y_val = list_columns_werte[int(value_column)]
    
    
    
    spy.stats.probplot(y, dist="norm", plot=plt)
    plt.show() 
    
   ################################################################################
   ###Log-file
    fname = 'Histogram by one factor'
    fvalue = 'Value: ' + y_val
    
    log = fname + '\n' + fvalue + '\n'
    session_write(log)

    

#######################################################################
###scatterplot
def scatter(df):
    clear()
    print('Simple Scatter Plot \n')        
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('x-value: \n(choose number) \n?')
        if value_column_x not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    
    y = list_columns_werte[int(value_column_y)]
    
    x = list_columns_werte[int(value_column_x)]
    
    
    
    #df.hist(column=y)
    df.plot.scatter(y,x) # Histogram will now be normalized
    label_chart = ('Scatter-Plot')
    plt.title(label_chart, fontdict=None, loc='center', pad=None)
    plt.show()

    ################################################################################
    ###Log-file
    fname = 'Scatterplot'
    fvalue = 'y-Value: ' + str(y)
    fbygroup = 'x-Value: ' + str(x)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n'
    session_write(log)


#######################################################################
###scatter plot with regression line
def scatter_w_r(df):
    clear()
    sns.set(color_codes=True)        
    
    print('Scatter Plot with Regression line linear \n')
    
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('x-value: \n(choose number) \n?')
        if value_column_x not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
        
    y = df[list_columns_werte[int(value_column_y)]]
    y_val = list_columns_werte[int(value_column_y)]
    x = df[list_columns_werte[int(value_column_x)]]
    x_val = list_columns_werte[int(value_column_x)]


    sns.regplot(x=x, y=y, data=df);


    
    label_chart = ('Linear-Regression-Plot')
    plt.title(label_chart, fontdict=None, loc='center', pad=None)
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Scatterplot'
    fvalue = 'y-Value: ' + y_val
    fbygroup = 'x-Value: ' + x_val
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n'
    session_write(log)
    
######################################################################
def scatter_by_o_factor(df):
    clear()
    print('scatter plot with one group')
    
    kategorie=df.select_dtypes(exclude=['float'])
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
        value_column_y = input('Column y-values: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('Column x-values: \n(choose number) \n?')
        if value_column_x not in list_number:
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
    
    y = list_columns_werte[int(value_column_y)]
    x = list_columns_werte[int(value_column_x)]
    f = list_columns_kategorie[int(groupby_column)]
    
    sns.lmplot(x=x, y=y, hue=f, data=df);
    
    plt.show()
    

#######################################################################
###jointplot
def scatter_joint_plot(df):
    clear()
    sns.set(color_codes=True)        
    print('Scatter Join Plot \n')
    
    
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('x-value: \n(choose number) \n?')
        if value_column_x not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    y = df[list_columns_werte[int(value_column_y)]]
    y_val = list_columns_werte[int(value_column_y)]
    x = df[list_columns_werte[int(value_column_x)]]
    x_val = list_columns_werte[int(value_column_x)]


    sns.jointplot(x=x, y=y, data=df, kind="reg");

    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Scatter-Joint-Plot'
    fvalue = 'y-Value: ' + y_val
    fbygroup = 'x-Value: ' + x_val
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n'
    session_write(log)

def bivariate_plot_w_m_elements (df):
    clear()
    
    print('Bivariate plot with multiple elements \n')
    
    sns.set_theme(style="dark")
    
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('x-value: \n(choose number) \n?')
        if value_column_x not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    y = list_columns_werte[int(value_column_y)]
    
    x = list_columns_werte[int(value_column_x)]
    
    
    # Draw a combo histogram and scatterplot with density contours
    f, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(x=x, y=y, s=5, color=".15", data = df)
    sns.histplot(x=x, y=y, bins=50, pthresh=.1, cmap="mako", data = df)
    sns.kdeplot(x=x, y=y, levels=5, color="w", linewidths=1, data = df)
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Bivariate Plot with Elements'
    fvalue = 'y-Value: ' + y
    fbygroup = 'x-Value: ' + x
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n'
    session_write(log)

def scatterplot_w_varying_point_sizes (df):
    clear()
    sns.set_theme(style="white")
    
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('x-value: \n(choose number) \n?')
        if value_column_x not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    while True:
        value_column_z= input('point-size-value: \n(choose number) \n?')
        if value_column_z not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
        
    y = df[list_columns_werte[int(value_column_y)]]
    y_val = list_columns_werte[int(value_column_y)]
    x = df[list_columns_werte[int(value_column_x)]]
    x_val =list_columns_werte[int(value_column_x)]
    z = df[list_columns_werte[int(value_column_z)]]
    z_val = list_columns_werte[int(value_column_z)]
    
    sns.relplot(x=x, y=y, size=z,
            sizes=(40, 400), alpha=.5, palette="muted",
            height=6, data=df)
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = '3D-Scatter Plot'
    fvalue = 'y-Value: ' + y_val
    fbygroup = 'x-Value: ' + x_val + '\nz-Value: ' + z_val
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n'
    session_write(log)
    
    
    
def scatterplot_w_varying_point_sizes_with_cat (df):
    
    clear()
    print('scatterplot with varying point sizes and category')
    
    sns.set_theme(style="white")
    
    werte = df.select_dtypes(exclude=['object'])
    kategorie=df.select_dtypes(exclude=['float'])
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('x-value: \n(choose number) \n?')
        if value_column_x not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    while True:
        value_column_z= input('point-size-value: \n(choose number) \n?')
        if value_column_z not in list_number:
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
    
    
    
    
    y = list_columns_werte[int(value_column_y)]
    
    x = list_columns_werte[int(value_column_x)]
    
    z = list_columns_werte[int(value_column_z)]

    c = list_columns_kategorie[int(groupby_column)]
    
    sns.relplot(x=x, y=y, size=z, hue=c,
            sizes=(40, 400), alpha=.5, palette="muted",
            height=6, data=df)
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Scatter Plot with varying point sizes and category'
    fvalue = 'y-Value: ' + y
    fbygroup = 'x-Value: ' + x + '\nz-Value: ' + z
    fcategory = 'Category: ' + c
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + fcategory + '\n'
    session_write(log)
    

#######################################################################
###Group Plot (show a plot by group)
def groupplot(df):
    clear()
    sns.set(style="ticks")
    print('Group -Plot')
    
    kategorie=df.select_dtypes(exclude=['float'])
    werte = df.select_dtypes(exclude=['object'])
    zeitraum=df.select_dtypes(exclude=['float'])
    
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
    
    anz_col_zeitraum = len(zeitraum.columns)
        
    list_columns_zeitraum = []
    list_number = []
    i=1
    for i in range(anz_col_zeitraum):
        list_columns_zeitraum.append(zeitraum.columns[i])
        list_number.append(str(i))
        print(i, zeitraum.columns[i])
        i+=1
    
    while True:
        datetime_column = input('Choose the X-axis-column \n(choose number) \n?')
        if datetime_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_kategorie[int(groupby_column)]
    z = list_columns_zeitraum[int(datetime_column)]
    
    df = df.sort_values(by=z, ascending=1)
    
    
    
    
    anz = df[x].nunique()    
    
    sns.relplot(x=z, y=y, hue=x, data=df, palette=sns.color_palette("Set1", anz))
    
    plt.xlim(df[list_columns_zeitraum[int(datetime_column)]].iloc[0], df[list_columns_zeitraum[int(datetime_column)]].iloc[-1])

    plt.show()

    ################################################################################
    ###Log-file
    fname = 'Scatter Plot with varying point sizes and category'
    fvalue = 'y-Value: ' + y
    fbygroup = 'x-Achse: ' + x 
    fcategory = 'Category: ' + z
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + fcategory + '\n'
    session_write(log)
    

#######################################################################
###Group Plot (show a plot by group with Tolerance)
def groupplot_w_T(df):
    clear()
    sns.set(style="ticks")

    print('Group Plot with Limit Line \n')
    kategorie=df.select_dtypes(exclude=['float'])
    werte = df.select_dtypes(exclude=['object'])
    zeitraum=df.select_dtypes(exclude=['float'])
    
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
    
    anz_col_zeitraum = len(zeitraum.columns)
        
    list_columns_zeitraum = []
    list_number = []
    i=1
    for i in range(anz_col_zeitraum):
        list_columns_zeitraum.append(zeitraum.columns[i])
        list_number.append(str(i))
        print(i, zeitraum.columns[i])
        i+=1
    
    while True:
        datetime_column = input('Choose the X-axis-column \n(choose number) \n?')
        if datetime_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_kategorie[int(groupby_column)]
    z = list_columns_zeitraum[int(datetime_column)]
    
    df = df.sort_values(by=z, ascending=1)
    
    
    
    
    anz = df[x].nunique()    
    
    
    while True:
        one_two_sided = input('Tolerance: \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
        nummer = [1,2,3]
        if int(one_two_sided) in nummer:
            break
        else:
            print('Wrong input, please try again')
    
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
    
    
    
    
        sns.relplot(x=z, y=y, hue=x, data=df, palette=sns.color_palette("Set1", anz))
        plt.axhline(y=ut,linewidth=2, color='r')
        
        plt.axhline(y=lt,linewidth=2, color='r')       
        plt.xlim(df[list_columns_zeitraum[int(datetime_column)]].iloc[0], df[list_columns_zeitraum[int(datetime_column)]].iloc[-1])
    
        plt.show()

    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
    
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                break
        
        
        ut = float(ut)
        lt = 'none'
        
        sns.relplot(x=z, y=y, hue=x, data=df, palette=sns.color_palette("Set1", anz))
        plt.axhline(y=ut,linewidth=2, color='r')
        plt.xlim(df[list_columns_zeitraum[int(datetime_column)]].iloc[0], df[list_columns_zeitraum[int(datetime_column)]].iloc[-1])
    
        plt.show()
        
    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
    
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                break
        
        
        
        
        ut = 'none'
        lt = float(lt)
        
        sns.relplot(x=z, y=y, hue=x, data=df, palette=sns.color_palette("Set1", anz))
        plt.axhline(y=lt,linewidth=2, color='r')
        plt.xlim(df[list_columns_zeitraum[int(datetime_column)]].iloc[0], df[list_columns_zeitraum[int(datetime_column)]].iloc[-1])
        
        plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Group Plot with Tolerance'
    fvalue = 'y-Value: ' + y
    fbygroup = 'x-Achse: ' + x 
    fcategory = 'Category: ' + z
    
    tol = 'Tolerance: ' + str(lt) + ';' + str(ut)

    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + fcategory + '\n' + tol + '\n'
    session_write(log)
    
    
def groupplot_menu(df):
    
    clear()
    print('Group Plot Menu \n')
    gp_menu = input('Which kind of Groupplot: \n1: Groupplot \n2: Groupplot with Toleranceline \n?')
    
    if gp_menu == '1':
        groupplot(df)
    elif gp_menu == '2':
        groupplot_w_T(df)
    else:
        print('wrong input (choose number), try again!')


###Init pareto
######################################################################
###Thanks to https://tylermarrs.com/posts/pareto-plot-with-matplotlib/
#####################################################################
def pareto_plot(df, x=None, y=None, title=None, show_pct_y=False, pct_format='{0:.0%}'):
    
    
    xlabel = x
    ylabel = y
    tmp = df.sort_values(y, ascending=False)
    x = tmp[x].values
    y = tmp[y].values
    weights = y / y.sum()
    cumsum = weights.cumsum()
    
    fig, ax1 = plt.subplots()
    ax1.bar(x, y)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    ax2 = ax1.twinx()
    ax2.plot(x, cumsum, '-ro', alpha=0.5)
    ax2.set_ylabel('', color='r')
    ax2.tick_params('y', colors='r')
    
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:,.2%}'.format(x) for x in vals])

    # hide y-labels on right side
    if not show_pct_y:
        ax2.set_yticks([])
    
    formatted_weights = [pct_format.format(x) for x in cumsum]
    for i, txt in enumerate(formatted_weights):
        ax2.annotate(txt, (x[i], cumsum[i]), fontweight='heavy')    
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    plt.show()

    ################################################################################
    ###Log-file
    fname = 'Pareto Chart count Column'
    fvalue = 'Column count: ' + str(y)
    
    
    log = fname + '\n' + fvalue + '\n'
    session_write(log)
    
#######################################################################    
###pareto plot with count column
def pareto(df):
    
    clear()
    print('Pareto Plot \n')
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
        value_column= input('Which value column do you want to see: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number = []
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
    
    df = df.groupby([x])[y].sum()
    df = df.reset_index()
    df= df.sort_values(y, ascending=False)
    df[x]=df[x].astype(str)
    
    print(df)
    pareto_plot(df, x=x, y=y, title='Pareto Chart')

    ################################################################################
    ###Log-file
    fname = 'Pareto Chart with value column'
    fvalue = 'y-Value: ' + str(y)
    fcategory = 'Category: ' + str(x)
       
    
    log = fname + '\n' + fvalue + '\n' + fcategory + '\n'
    session_write(log)
    

#######################################################################
###single pareto plot, count the entrees of column    
def pareto_one_column(df):
    
    clear()
    print('Pareto Plot \n')
    werte = df.select_dtypes(exclude=['float'])
    
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
        value_column= input('Which value column do you want to see: \n(choose number) \n?')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    y = list_columns_werte[int(value_column)]
    
    
    
    df2 = df[y].value_counts()
    df2 = df2.reset_index()
    x = 'index'
    
    df2= df2.sort_values([y], ascending=False)
    df2[x]=df2[x].astype(str)
    
    
    print(df2)
    pareto_plot(df2, x=x, y=y, title='Pareto Chart')


def three_d_scatterplot(df):
    clear()
    
    
    print('3D Scatter Plot \n')
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('x-value: \n(choose number) \n?')
        if value_column_x not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    while True:
        value_column_z= input('z-value: \n(choose number) \n?')
        if value_column_z not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
        
    y = df[list_columns_werte[int(value_column_y)]]
    y_val =list_columns_werte[int(value_column_y)]
    x = df[list_columns_werte[int(value_column_x)]]
    x_val = list_columns_werte[int(value_column_x)]
    z = df[list_columns_werte[int(value_column_z)]]
    z_val = list_columns_werte[int(value_column_z)]
    
    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z)
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = '3D Scatter Plot'
    fvalue = 'y-Value: ' + y_val
    fbygroup = 'x-Value: ' + x_val + '\nz-Value: ' + z_val
    
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n'
    session_write(log)
    
    
    
    
def trisurfaceplot(df):
    clear()
    
    
    print('3D Surface Plot \n')
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break  
    while True:
        value_column_x= input('x-value: \n(choose number) \n?')
        if value_column_x not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    while True:
        value_column_z= input('z-value: \n(choose number) \n?')
        if value_column_z not in list_number:
            print('wrong input, try again!')
        else:
            break  
        
        
    y = df[list_columns_werte[int(value_column_y)]]
    y_val = list_columns_werte[int(value_column_y)]
    x = df[list_columns_werte[int(value_column_x)]]
    x_val = list_columns_werte[int(value_column_x)]
    z = df[list_columns_werte[int(value_column_z)]]
    z_val = list_columns_werte[int(value_column_z)]
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    
    ax.plot_trisurf(x, y, z, linewidth=0, antialiased=False)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = '3D Surface Plot'
    fvalue = 'y-Value: ' + y_val
    fbygroup = 'x-Value: ' + x_val + '\nz-Value: ' + z_val
    
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n'
    session_write(log)
    
    
    
def threeddplot(df):
    clear()
    
    print('3D Plot Menue \n')
    tdplot = input('Choose 3d-Plot: \n1: 3d-scatter-plot \n2: 3d-surface-plot \n?')
    
    if tdplot == '1':
        three_d_scatterplot(df)
    elif tdplot == '2':
        trisurfaceplot(df)
    else:
        print('wrong input, please try again')

#############################################################################
def decriptive_statistics(df):
    
    #df['number'] = range(1, len(df) + 1)
    
    clear()
    print('Descriptive Statistic \n')
    werte = df.select_dtypes(include=['float', 'int', 'int64'])
    
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
        value_column_y= input('y-value: \n(choose number) \n?')
        if value_column_y not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    df['number'] = range(1, len(df) + 1)
    
    y = df[list_columns_werte[int(value_column_y)]]
    y_val = list_columns_werte[int(value_column_y)]
    x = df['number']
    stat, p = shapiro(y)
            
    ###one side tolerance ut / normal distribution
    if p >= 0.05:
        #normal verteilt
        print('normal distribution')
        
        mean_y = y.mean()
        std_y = y.std()
        count_y = len(y)
        mean_p_3s = mean_y + 3*std_y
        mean_m_3s = mean_y - 3*std_y
        min_y = y.min()
        max_y = y.max()
        
        t_mean_y = truncate(mean_y, 5)
        t_std_y = truncate(std_y, 5)
        t_mean_p_3s = truncate(mean_p_3s, 5)
        t_mean_m_3s = truncate(mean_m_3s, 5)
        
        text = 'distribution should follow normal distribution'
        
        
        
        
        eintrag = 'Mean: ' + str(t_mean_y) + '\ns: ' + str(t_std_y) + '\n \n+3s: ' + str(t_mean_p_3s) + '\n-3s: ' + str(t_mean_m_3s) + '\n \nMIN: ' + str(min_y) + '\nMAX: '+ str(max_y) + '\nn: ' + str(count_y) + '\n\n' + text
        
        print(eintrag +'\np-value:' + str(p))
        ##graphic
                
        plt.figure(figsize=(6, 4))
        plt.subplot(221) # äquivalent zu: plt.subplot(2, 2, 1)
        sns.histplot(y, kde=True)
        plt.subplot(222)
        sns.lineplot(x=x, y=y_val, estimator=None, lw=1, marker='o', data=df)
        #df.plot(y_val)
        plt.axhline(y=mean_y,linewidth=2, color='g')
        plt.axhline(y=mean_p_3s,linewidth=2, color='orange')
        plt.axhline(y=mean_m_3s,linewidth=2, color='orange')
        plt.subplot(223)
        sns.boxplot(x=y)
        plt.subplot(224)
        plt.text(0.1,0.5,eintrag, 
                 ha='left', va='center',
                 fontsize=12)
        plt.axis('off')
        #plt.title(label_chart, fontdict=None, loc='center', pad=None)
        plt.show()
        
    else:
        
        median_y = y.quantile(0.5)
                
        upper_q_y = y.quantile(0.99869)
                
        lower_q_y = y.quantile(0.00135)
        min_y = y.min()
        max_y = y.max()
                
        median_y = truncate(median_y, 5)
        upper_q_y = truncate(upper_q_y, 5)
        lower_q_y = truncate(lower_q_y, 5)
        min_y = truncate(min_y, 5)
        max_y =truncate(max_y, 5)
        count_y = len(y)
        
        text = 'distribution should not follow normal distribution'
        
        
        
        
        eintrag = 'Median: ' + str(median_y) + '\n\nQ0.998: '  + str(upper_q_y) + '\nQ0.001: ' + str(lower_q_y) + '\n \nMIN: ' + str(min_y) + '\nMAX: '+ str(max_y) + '\nn: ' + str(count_y) + '\n\n' + text
        
        print(eintrag +'\np-value:' + str(p))
        
        ##graphic
                
        plt.figure(figsize=(6, 4))
        plt.subplot(221) # äquivalent zu: plt.subplot(2, 2, 1)
        sns.histplot(y, kde=True)
        plt.subplot(222)
        sns.lineplot(x=x, y=y_val, estimator=None, lw=1, marker='o', data=df)
        #df.plot(y_val)
        plt.axhline(y=median_y,linewidth=2, color='g')
        plt.axhline(y=upper_q_y,linewidth=2, color='orange')
        plt.axhline(y=lower_q_y,linewidth=2, color='orange')
        plt.subplot(223)
        sns.boxplot(x=y)
        plt.subplot(224)
        plt.text(0.1,0.5,eintrag, 
                 ha='left', va='center',
                 fontsize=12)
        plt.axis('off')
        #plt.title(label_chart, fontdict=None, loc='center', pad=None)
        plt.show()

    ################################################################################
    ###Log-file
    fname = 'Graphical descriptive statistic'
    fvalue = 'y-Value: ' + y_val
    
    
    
    log = fname + '\n' + fvalue + '\n' + eintrag + '\np-Value (shapiro wilk test): ' + str(p)
    session_write(log)


        
def easy_pairplot(df):
    clear()
    print('easy Pair Plot \n \nAttention!! \n This plot needs cpu resources and cold take a few minutes! \n')    
        
    g = sns.PairGrid(df)
    g.map(sns.scatterplot)
    
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Easy Pairplot'
    fvalue = 'over all values'
    
    
    
    log = fname + '\n' + fvalue + '\n' 
    session_write(log)
    
    
    
    
def pairplot_hist(df):
    clear()
    
    print('Pair Plot with Histogram \n \nAttention!! \n This plot needs cpu resources and cold take a few minutes! \n')
    
    g = sns.PairGrid(df)
    g.map_diag(sns.histplot)
    g.map_offdiag(sns.scatterplot)
    plt.show()

    ################################################################################
    ###Log-file
    fname = 'Pairplot with Histogram'
    fvalue = 'over all values'
    
    
    
    log = fname + '\n' + fvalue + '\n' 
    session_write(log)
    

def pairplot_dist(df):
    clear()
    print('Pair Plot with distribution \n \nAttention!! \n This plot needs cpu resources and cold take a few minutes! \n')

    g = sns.PairGrid(df)
    g.map_upper(sns.scatterplot)
    g.map_lower(sns.kdeplot)
    g.map_diag(sns.kdeplot, lw=3, legend=False)
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Pairplot with Distribution-Chart'
    fvalue = 'over all values'
    
    
    
    log = fname + '\n' + fvalue + '\n' 
    session_write(log)

def pairplot_1c (df):
    clear()
    print('Pair Plot with group \n \nAttention!! \n This plot needs cpu resources and cold take a few minutes! \n')
    
    
    category=df.select_dtypes(exclude=['float'])
    
    anz_col_category = len(category.columns)
        
    list_columns_category = []
    list_number=[]
    i=1
    for i in range(anz_col_category):
        list_columns_category.append(category.columns[i])
        list_number.append(str(i))
        print(i, category.columns[i])
        i+=1
    
    while True:
        groupby_column = input('Group by column: \n(choose number) \n?')
        if groupby_column not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    x = list_columns_category[int(groupby_column)]
    
    print('easy Pair Plot \n \nAttention!! \n This plot needs cpu resources and cold take a few minutes! \n')
    g = sns.PairGrid(df, hue=x)
    g.map(sns.scatterplot)
    
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Pairplot with Catogory'
    fvalue = 'over all values'
    fbygroup = 'Category: ' + x
    
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' 
    session_write(log)
    
def pairplot_1c_hist(df):
    clear()
    print('Pair Plot with group and histogram \n \nAttention!! \n This plot needs cpu resources and cold take a few minutes! \n')
    
    category=df.select_dtypes(exclude=['float'])
    
    anz_col_category = len(category.columns)
        
    list_columns_category = []
    list_number=[]
    i=1
    for i in range(anz_col_category):
        list_columns_category.append(category.columns[i])
        list_number.append(str(i))
        print(i, category.columns[i])
        i+=1
    
    while True:
        groupby_column = input('Group by column: \n(choose number) \n?')
        if groupby_column not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    x = list_columns_category[int(groupby_column)]
    
    
    g = sns.PairGrid(df, hue=x)
    g.map_diag(sns.histplot)
    g.map_offdiag(sns.scatterplot)
    g.add_legend()
    
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Pairplot with Catogory and Histogram'
    fvalue = 'over all values'
    fbygroup = 'Category: ' + x
    
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' 
    session_write(log)
    
def pairplot_1c_dist(df):
    clear()
    print('Pair Plot with group and distribution plot \n \nAttention!! \n This plot needs cpu resources and cold take a few minutes! \n')
    
    
    category=df.select_dtypes(exclude=['float'])
    
    anz_col_category = len(category.columns)
        
    list_columns_category = []
    list_number=[]
    i=1
    for i in range(anz_col_category):
        list_columns_category.append(category.columns[i])
        list_number.append(str(i))
        print(i, category.columns[i])
        i+=1
    
    while True:
        groupby_column = input('Group by column: \n(choose number) \n?')
        if groupby_column not in list_number:
            print('wrong input, try again!')
        else:
            break
    
    x = list_columns_category[int(groupby_column)]
    
    sns.pairplot(df, hue=x, height=2.5)
    
    plt.show()
    
    ################################################################################
    ###Log-file
    fname = 'Pairplot with Catogory and Distribution'
    fvalue = 'over all values'
    fbygroup = 'Category: ' + x
    
    
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' 
    session_write(log)
    
    
def pairplot_menu(df):
    clear()
    print('Pair Scatter Plot Menue \n')
    pp_menu = input('Wich kind of pair plot?: \n1: simple pair plot \n2: pairplot with histogram \n3: pairplot with distribution plot \n4: pairplot with categorie \n5: pairplot with histogram and categorie \n6: pairplot with disribution and categorie \n?')
    if pp_menu == '1':
        easy_pairplot(df)
    elif pp_menu == '2':
        pairplot_hist(df)
    elif pp_menu == '3':
        pairplot_dist(df)
    elif pp_menu == '4':
        pairplot_1c (df)
    elif pp_menu == '5':
        pairplot_1c_hist(df)
    elif pp_menu == '6':
        pairplot_1c_dist(df)
    else:
        print('wrong input (choose number), try again!')
        
def cond_mean_w_ob_by_1f (df):
    clear()
    
    print('Conditional mean with observation by 1 factor \n')
    sns.set_theme(style="whitegrid")
    
    kategorie=df.select_dtypes(exclude=['float'])
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
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        
        # Initialize the figure
        f, ax = plt.subplots()
        sns.despine(bottom=True, left=True)
    
    
        # Show each observation with a scatterplot
        sns.stripplot(x=x, y=y, 
              data=df, dodge=True, alpha=.25, zorder=1)   

        # Show the conditional means
        sns.pointplot(x=x, y=y,
              data=df, dodge=.532, join=False, palette="dark",
              markers="d", scale=.75, ci=None)         
    
        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            
            # Initialize the figure
            f, ax = plt.subplots()
            sns.despine(bottom=True, left=True)
    
    
            # Show each observation with a scatterplot
            sns.stripplot(x=x, y=y, 
                          data=df, dodge=True, alpha=.25, zorder=1)   

            # Show the conditional means
            sns.pointplot(x=x, y=y,
                          data=df, dodge=.532, join=False, palette="dark",
                          markers="d", scale=.75, ci=None)         
        
            plt.axhline(y=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            
            # Initialize the figure
            f, ax = plt.subplots()
            sns.despine(bottom=True, left=True)
    
    
            # Show each observation with a scatterplot
            sns.stripplot(x=x, y=y, 
                          data=df, dodge=True, alpha=.25, zorder=1)   

            # Show the conditional means
            sns.pointplot(x=x, y=y,
                          data=df, dodge=.532, join=False, palette="dark",
                          markers="d", scale=.75, ci=None)         
        
            plt.axhline(y=lt,linewidth=2, color='red')
            
            
            plt.show()
        
        else:
        
            
            # Initialize the figure
            f, ax = plt.subplots()
            sns.despine(bottom=True, left=True)
    
    
            # Show each observation with a scatterplot
            sns.stripplot(x=x, y=y, 
                          data=df, dodge=True, alpha=.25, zorder=1)   

            # Show the conditional means
            sns.pointplot(x=x, y=y,
                          data=df, dodge=.532, join=False, palette="dark",
                          markers="d", scale=.75, ci=None)         
        
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            
            plt.show()
    
    ################################################################################
###Log-file
    fname = 'Conditional mean with observation by 1 factor'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)

    

def cond_mean_w_ob_by_2f (df):
    clear()
    
    print('Conditional mean with observation by 2 factors \n')
    
    sns.set_theme(style="whitegrid")
    
    kategorie=df.select_dtypes(exclude=['float'])
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
        groupby_column = input('Group 1 by column: \n(choose number) \n?')
        if groupby_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
       
    
    while True:
        groupby_column2 = input('Group 2 by column: \n(choose number) \n?')
        if groupby_column2 not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
    
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_kategorie[int(groupby_column)]
    z = list_columns_kategorie[int(groupby_column2)]
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        
        # Initialize the figure
        f, ax = plt.subplots()
        sns.despine(bottom=True, left=True)
    
    
        # Show each observation with a scatterplot
        sns.stripplot(x=x, y=y, hue=z,
              data=df, dodge=True, alpha=.25, zorder=1)   

        # Show the conditional means
        sns.pointplot(x=x, y=y,hue=z,
              data=df, dodge=.532, join=False, palette="dark",
              markers="d", scale=.75, ci=None)         
    
        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            
            # Initialize the figure
            f, ax = plt.subplots()
            sns.despine(bottom=True, left=True)
    
    
            # Show each observation with a scatterplot
            sns.stripplot(x=x, y=y,hue=z, 
                          data=df, dodge=True, alpha=.25, zorder=1)   

            # Show the conditional means
            sns.pointplot(x=x, y=y,hue=z,
                          data=df, dodge=.532, join=False, palette="dark",
                          markers="d", scale=.75, ci=None)         
        
            plt.axhline(y=ut,linewidth=2, color='red')
            
            
            # Improve the legend 
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[3:], labels[3:], title=z,
                      handletextpad=0, columnspacing=1,
                      loc="lower right", ncol=3, frameon=True)
            
            plt.show()
            
        elif ut=='none':
            
            
            # Initialize the figure
            f, ax = plt.subplots()
            sns.despine(bottom=True, left=True)
    
    
            # Show each observation with a scatterplot
            sns.stripplot(x=x, y=y,hue=z, 
                          data=df, dodge=True, alpha=.25, zorder=1)   

            # Show the conditional means
            sns.pointplot(x=x, y=y,hue=z,
                          data=df, dodge=.532, join=False, palette="dark",
                          markers="d", scale=.75, ci=None)         
        
            plt.axhline(y=lt,linewidth=2, color='red')
            
            # Improve the legend 
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[3:], labels[3:], title=z,
                      handletextpad=0, columnspacing=1,
                      loc="lower right", ncol=3, frameon=True)
            
            plt.show()
        
        else:
        
            
            # Initialize the figure
            f, ax = plt.subplots()
            sns.despine(bottom=True, left=True)
    
    
            # Show each observation with a scatterplot
            sns.stripplot(x=x, y=y, hue=z, 
                          data=df, dodge=True, alpha=.25, zorder=1)   

            # Show the conditional means
            sns.pointplot(x=x, y=y,hue=z,
                          data=df, dodge=.532, join=False, palette="dark",
                          markers="d", scale=.75, ci=None)         
        
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            
            # Improve the legend 
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[3:], labels[3:], title=z,
                      handletextpad=0, columnspacing=1,
                      loc="lower right", ncol=3, frameon=True)
            
            plt.show()

        ################################################################################
###Log-file
    fname = 'Conditional mean with observation by 2 factors'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x + ' and ' + z
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)

                  
            
def stacked_hist (df):
    clear()
    
    print('stacked Histogram by one catogorie \n')
    
    #sns.set_theme(style="ticks")
    sns.set_theme(style="whitegrid")
    
    kategorie=df.select_dtypes(exclude=['float'])
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
    
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        
        f, ax = plt.subplots(figsize=(7, 5))
        sns.despine(f)

        sns.histplot(
                df,
                x=y, hue=x,
                multiple="stack",
                palette="light:m_r",
                edgecolor=".3",
                linewidth=.5
        )
        
        
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            
            f, ax = plt.subplots(figsize=(7, 5))
            sns.despine(f)

            sns.histplot(
                df,
                x=y, hue=x,
                multiple="stack",
                palette="light:m_r",
                edgecolor=".3",
                linewidth=.5
            )
        
        
                
        
            plt.axhline(x=ut,linewidth=2, color='red')
            
            
            plt.show()
            
        elif ut=='none':
            
            
            f, ax = plt.subplots(figsize=(7, 5))
            sns.despine(f)

            sns.histplot(
                df,
                x=y, hue=x,
                multiple="stack",
                palette="light:m_r",
                edgecolor=".3",
                linewidth=.5
            )
            
            plt.axvline(x=lt,linewidth=2, color='red')
            plt.show()
        
        else:
        
            
            f, ax = plt.subplots(figsize=(7, 5))
            sns.despine(f)

            sns.histplot(
                df,
                x=y, hue=x,
                multiple="stack",
                palette="light:m_r",
                edgecolor=".3",
                linewidth=.5
            )

        
            plt.axvline(x=ut,linewidth=2, color='red')
            plt.axvline(x=lt,linewidth=2, color='red')
            
            plt.show()
    
    
            ################################################################################
###Log-file
    fname = 'Stacked Histogram'
    fvalue = 'Value: ' + y
    fbygroup = 'Group by: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)

###
#time series plot
def time_series_plot(df):
    clear()
    print('Time Series Plot')
    
    kategorie=df.select_dtypes(include=['object', 'datetime', 'int'])
    werte = df.select_dtypes(exclude=['object'])
    
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number = []
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    
    while True:
        value_column= input('Which value column do you want to see: \n(choose number)\n')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number = []
    i=1
    
    for i in range(anz_col_kategorie):
        list_columns_kategorie.append(kategorie.columns[i])
        list_number.append(str(i))
        print(i, kategorie.columns[i])
        i+=1
    
    
    while True:
        groupby_column = input('Date/Time column: \n(choose number) \n?')
        if groupby_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
       
    
          
    
    y = list_columns_werte[int(value_column)]
    x = list_columns_kategorie[int(groupby_column)]
    
    
    try:
        df[x] = df[x].astype('datetime64[ns]')
        
    except Exception as exception:
        print('With the current Datatype - Convert data into DateTime Format is not possible! \nPlease use first the Convert Data Format function under the Table Functions.')
    
    df = df.sort_values(by=x, ascending=1)
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        
        dots_yes = input('Graph with dots: y/n \n?')
        if dots_yes =='y':
            sns.lineplot(data = df, x=x, y=y, marker='o')
        else:
            sns.lineplot(data = df, x=x, y=y)
        
        plt.xticks(rotation=25)
        plt.show()
        
    else:
        
    
        if lt =='none':
              
            dots_yes = input('Graph with dots: y/n \n?')
            if dots_yes =='y':
                
                sns.lineplot(data = df, x=x, y=y, marker='o')
            else:
                sns.lineplot(data = df, x=x, y=y)
        
            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=25)
            plt.show()
            
        elif ut=='none':
            
            dots_yes = input('Graph with dots: y/n \n?')
            if dots_yes =='y':
                sns.lineplot(data = df, x=x, y=y, marker='o')
            else:
                sns.lineplot(data = df, x=x, y=y)
        
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=25)
            plt.show()
        
        
        else:
        
            dots_yes = input('Graph with dots: y/n \n?')
            if dots_yes =='y':
                sns.lineplot(data = df, x=x, y=y, marker='o')
            else:
                sns.lineplot(data = df, x=x, y=y)
        
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=25)
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Time Series Plot'
    fvalue = 'Value: ' + y
    fbygroup = 'Time-Axis: ' + x
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + tol + '\n'
    session_write(log)

###
#time series plot by category

def time_series_plot_cat(df):
    clear()
        
    print('Time Series Plot')
    
    kategorie=df.select_dtypes(include=['object', 'datetime', 'int'])
    werte = df.select_dtypes(exclude=['object'])
    
    
    #
    anz_col_werte = len(werte.columns)
        
    list_columns_werte = []
    list_number = []
    i=1
    for i in range(anz_col_werte):
        list_columns_werte.append(werte.columns[i])
        list_number.append(str(i))
        print(i, werte.columns[i])
        i+=1
    
    
    while True:
        value_column= input('Which value column do you want to see: \n(choose number)\n')
        if value_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    clear()
    #
    anz_col_kategorie = len(kategorie.columns)
        
    list_columns_kategorie = []
    list_number = []
    i=1
    
    for i in range(anz_col_kategorie):
        list_columns_kategorie.append(kategorie.columns[i])
        list_number.append(str(i))
        print(i, kategorie.columns[i])
        i+=1
    
    
    while True:
        groupby_column = input('Date/Time column: \n(choose number) \n?')
        if groupby_column not in list_number:
            print('wrong input, try again!')
        else:
            break  
    
    
       
    
    while True:
        groupby_column1 = input('Categorie column: \n(choose number) \n?')
        if groupby_column1 not in list_number:
            print('wrong input, try again!')
        else:
            break  
          
    z = list_columns_kategorie[int(groupby_column1)]
    y = list_columns_werte[int(value_column)]
    x = list_columns_kategorie[int(groupby_column)]
    
    
    try:
        df[x] = df[x].astype('datetime64[ns]')
        
    except Exception as exception:
        print('With the current Datatype - Convert data into DateTime Format is not possible! \nPlease use first the Convert Data Format function under the Table Functions.')
    
    df = df.sort_values(by=x, ascending=1)
    
    ###toleranzen
    one_two_sided = input('Tolerance: \n0: no tolerance \n1: both side tolerance \n2: one side ut \n3: one side lt \n(choose number) \n?')
    
    notol = '0'
    ###both side tolerance
    if one_two_sided == '1':
        
        while True:
            tol = input('upper tolerance , lower tolerance \n(choose point-comma / seperate with float-comma, example:2.2 , 1.9) \n?')
            if ',' in tol:
                try:
                    ut, lt = tol.split(',')
                    ut = float(ut)
                    lt = float(lt)
                    if lt > ut:
                        print('ut<lt, wrong input!')
                    else:                    
                        break
                except Exception as exception:
                    print('Wrong input, try again!')
            else:
                print('wrong input, separator is missing!, please try again!')
        
        print(ut,lt)
        
     
    ###one side tolerance ut
    elif one_two_sided =='2':
        
        
        while True:
            ut = input('Upper tolerance: \n(choose point-comma) \n?')
            ut = float(ut)
            if not isfloat(ut):
                print("target mean value is not a number with point-comma, please try again")
            else:
                lt = 'none'
                break
                
                

    ###one side tolerance lt
    elif one_two_sided =='3':
        
        while True:
            lt = input('Lower tolerance: \n(choose point-comma) \n?')
            lt = float(lt)
            if not isfloat(lt):
                print("target mean value is not a number with point-comma, please try again")
            else:
                ut = 'none'
                break
            
                
                
    else:
        notol = '1'
            
    if notol =='1':
        
        dots_yes = input('Graph with dots: y/n \n?')
        if dots_yes =='y':
            sns.lineplot(data = df, x=x, y=y, marker='o', hue=z)
        else:
            sns.lineplot(data = df, x=x, y=y, hue=z)
        
        plt.xticks(rotation=25)
        

        plt.show()
        
    else:
        
    
        if lt =='none':
              
            dots_yes = input('Graph with dots: y/n \n?')
            if dots_yes =='y':
                
                sns.lineplot(data = df, x=x, y=y, marker='o', hue =z)
            else:
                sns.lineplot(data = df, x=x, y=y, hue=z)
        
            
            plt.axhline(y=ut,linewidth=2, color='red')
            
            plt.xticks(rotation=25)
            
            plt.show()
            
        elif ut=='none':
            
            dots_yes = input('Graph with dots: y/n \n?')
            if dots_yes =='y':
                sns.lineplot(data = df, x=x, y=y, marker='o', hue = z)
            else:
                sns.lineplot(data = df, x=x, y=y, hue = z)
        
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=25)
            plt.xlabel("Height", size=11)
            plt.show()
        
        
        else:
        
            dots_yes = input('Graph with dots: y/n \n?')
            if dots_yes =='y':
                sns.lineplot(data = df, x=x, y=y, marker='o', hue = z)
            else:
                sns.lineplot(data = df, x=x, y=y, hue = z)
        
            plt.axhline(y=ut,linewidth=2, color='red')
            plt.axhline(y=lt,linewidth=2, color='red')
            plt.xticks(rotation=25)
            
            plt.show()
    
    
    ###########################################################################
    ###session-datei
    
    fname = 'Time Series Plot by Factor'
    fvalue = 'Value: ' + y
    fbydate = 'Time-Axis: ' + x
    fbygroup = 'by factor: ' + z
    if notol =='1':
        tol ='no tolerances set'
    else:
        tol = 'Tolerance: ' + str(lt) + ';' + str(ut)
    
    log = fname + '\n' + fvalue + '\n' + fbygroup + '\n' + fbydate + '\n' + tol + '\n'
    session_write(log)

def time_s_plot_menu(df):
    clear()
    tsp_menu = input('Time series plot Menu: \n1: Time series plot \n2: Time series plot by factor \n?')
    if tsp_menu == '1':
        time_series_plot(df)
    elif tsp_menu == '2':
        time_series_plot_cat(df)
    else:
        print('wrong input, please try again!')
    