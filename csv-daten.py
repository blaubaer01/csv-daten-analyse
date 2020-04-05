import pandas as pd
#import shutil
import os
#import datetime
#import tkinter as tk
# import only system from os 
from os import system, name 


#Alternativquelle definieren
source='daten.csv'

#Quelle waehlen und als "source" speichern
def csv_daten_im_verzeichnis():
    csv_dateien = []
    for dat in os.listdir(os.getcwd()):
        if dat.endswith(".csv") or dat.endswith(".CSV"):
            csv_dateien.append(dat)
    print(csv_dateien)
    return(csv_dateien)
            
        


def file_einlesen(auswahl_datei):
    
    #Format festlegen
    format_ist = input('Welches Trennzeichen nutzt die Datei \na:Komma / b:Semikolon \n?').lower()
    if format_ist == 'a':
        trennzeichen = ','
        dezimalzeichen = '.'
    elif format_ist == 'b':
        trennzeichen = ';'
        dezimalzeichen =','
    else:
        trennzeichen =','
        dezimalzeichen ='.'
    
    #print(trennzeichen, " ", dezimalzeichen)
    #Kopfzeile
    kopfzeile = input('Gibt es eine Kopfzeile \n j/n \n ?').lower()
    if kopfzeile == 'j':
        kopfz = 0
    elif kopfzeile =='n':
        kopfz = None
        
    
    #Dateieinlesen
    df=pd.read_csv(auswahl_datei,sep=trennzeichen ,decimal=dezimalzeichen, header=kopfz)
    #print(csv_daten)
    
    return(df)


# define our clear function 
def clear(): 
  
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

# all single data
def ind_trip_data(df):
    y=0
    while y < (len(df)):
        a = y
        for i in range(5):
            print(df.iloc[a,:])
            a +=1
        y += 5
                   
        end_data = input("Next single Data? type 'enter' for yes or 'n' for no \n?")
        if (len(df)) <y+5:
            rest = abs((len(df))-y)
            #print(rest, y)
            for i in range(rest):
                print(df.iloc[a,:])
                a +=1
            print('Das Ende der Tabelle ist erreicht !')
            break
        if end_data.lower() == 'n':
            break
        
#Kopfzeile und erste Daten anschauen
def first_row(df):
    print(df.iloc[0,:])
    

#Einzeldaten anschauen
def einzeldaten_anschauen(df):
    eind = input('Was möchten Sie sehen \n1: erste Reihe\n2: alles je 5 Reihen\n?' )
    if eind=='1':
        first_row(df)
    elif eind =='2':
        ind_trip_data(df)
    else:
        first_row(df)
        
# Einfache beschreibende Statitik        
def beschreibende_stat(df):
    print('Beschreibende Statistik \n', df.describe())

def statistic(df):
    menu_statistic = input('Welche Art der Statistik: \n1:Beschreibende Statistik \n2:Grafische Darstellung \n?')
    if menu_statistic =='1':
        beschreibende_stat(df)
        
def fehlende_daten(df):
    print('Überprüfung auf fehlende Daten ergab folgendes Ergebnis: \n',    df.isnull().sum())

def datentyp(df):
    print('Überischt der Datenformate: \n', df.dtypes)

def mit_daten_arbeiten(df):
    while True:
        clear()
        show_or_statistic = input('Was möchtest du dir anschauen: \n1:Einzeldaten \n2:Datenfromat \n3:fehlenede Daten? \n4:Statistik \n?')
        if show_or_statistic =='1':
            clear()
            einzeldaten_anschauen(df)
        elif show_or_statistic =='2':
            clear()
            datentyp(df)
        elif show_or_statistic =='3':
            clear()
            fehlende_daten(df)
        elif show_or_statistic =='4':
            clear()
            statistic(df)
        restart = input('\nMöchtest du weiter analysieren? j/n.\n?')
        if restart.lower() != 'j':
            break
        


# Programm-Ablauf
def main():
    while True:
        clear()
        #choosesource(source)
        print('#'*70)
        print('Folgende CSV-Dateien zur zur Auswahl, welche möchten sie auswerten?')
        csv_daten_im_verzeichnis()    
    
        #print(csv_dateien)
        auswahl_datei = input('Welche Daten einlesen ? :')
        df=file_einlesen(auswahl_datei)
        
        clear()
    
        print('#'*70)
        
        mit_daten_arbeiten(df)
                   
        
        restart = input('\nMöchtest du eine weitere CSV-Datei analysieren? j/n.\n?')
        if restart.lower() != 'j':
            break
          




#Hauptprozesse starten
if __name__ == '__main__':
    main()
    
    