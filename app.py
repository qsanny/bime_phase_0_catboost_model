import pandas as pd
import requests
import pyodbc
import os
import time
import random

import json

DATABASE_FILE_PATH = r'DBQ=C:/Users/Qadir/Documents/notebooks/BDD_CCG_BIME3.accdb;'
DRIVER = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
conn_str = ( DRIVER + DATABASE_FILE_PATH)
TABLE_NAME = "BIME"

cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()

# Liste des tables
# for table_info in cursor.tables(tableType='TABLE'):
#     print(table_info.table_name)
print("connection succced")

def request(data):

    # api-endpoint
    URL = "http://bc8f-35-230-17-155.ngrok.io"
    
    # location given here
    location = "delhi technological university"
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'input':f"{data}"}
    
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params=PARAMS)
    
    # extracting data in json format
    data = r.json()
   # print(data)
    return data


class Data:
    def __init__(self, o):
        self.Rating_societe = o.Rating_societe
        self.Travaux_etat_ou_entreprise_generale = 1 if o.Travaux_etat_ou_entreprise_generale else 0
        self.Taux_precommercialisation = o.Taux_precommercialisation
        self.Vente_en_bloc = 1 if o.Vente_en_bloc else 0
        self.Ratio_FP_MI = o.Ratio_FP_MI
        self.Taux_Souscription = o.Taux_Souscription
        self.Lancement_BIME = o.Lancement_BIME

    def fit(self):
        data = f"{self.Taux_Souscription},{self.Rating_societe},{self.Travaux_etat_ou_entreprise_generale},{self.Taux_precommercialisation},{self.Vente_en_bloc},{self.Ratio_FP_MI}"
        y = request(data)
        if y is not None:
            print(y['y'])
            self.Taux_Souscription = y['y']

        # self.result = o.result

class Monkey(object):
    def __init__(self, filename, fn):
        self._cached_stamp = 0
        self.filename = filename
        self.fn = fn

    def watch(self):
        while(True):
            stamp = os.stat(self.filename).st_mtime
            # print(stamp)
            if stamp > self._cached_stamp:
                self.fn()
                self._cached_stamp = stamp
            time.sleep(0.5)


def get_one_data(id = 1):
    table1_data_query = f"SELECT * from {TABLE_NAME}"
    cursor.execute(table1_data_query)
    first_row =  cursor.fetchone()
    print(first_row)
    return Data(first_row)

def update_result(result):
    table1_insert_data = f"""
    UPDATE {TABLE_NAME} 
    SET Taux_Souscription = {result}, Lancement_BIME = False
    """
    with cnxn:
        cursor.execute(table1_insert_data)
        print('updated')

def check_and_update():
    data: "Data" = get_one_data(1)
    if data.Lancement_BIME:
        data.fit();
        update_result(data.Taux_Souscription)

mk = Monkey("BDD_CCG_BIME3.accdb", check_and_update)

mk.watch()
