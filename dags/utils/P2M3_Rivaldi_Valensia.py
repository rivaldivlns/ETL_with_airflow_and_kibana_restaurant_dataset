'''
=================================================
Milestone 3

Name: Rivaldi Valensia
Batch: FTDS-007-HCK

Program ini dibuat untuk melakukan automatisasi transform dan load datamenggunakan PostgreSQL, Airflow dan Visualisasi menggunakan ElasticSearch& Kibana. 
Adapun dataset yang digunakan adalah dataset mengenai data restaurant.
=================================================
'''

import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

# Function to get data from PostgreSQL
def get_data_from_postgresql():
    conn_string = "dbname='airflow' host='postgres' user='airflow' password='airflow'"
    conn = db.connect(conn_string)
    df = pd.read_sql("select * from public.table_m3", conn)  # Updated table name to 'public.table_m3'
    df.to_csv('/opt/airflow/data/P2M3_Valdi_data_raw.csv',index=False)

# Function to clean the DataFrame
def clean_dataframe():
    df = pd.read_csv('/opt/airflow/data/P2M3_Valdi_data_raw.csv')

    # Mengganti spasi dengan underscore pada nama kolom
    df.columns = df.columns.str.replace(' ', '_')
    
    # Mengonversi tipe data kolom 'price' dan 'average_ratings' menjadi integer
    df['price'] = df['price'].astype(int)
    df['average_ratings'] = df['average_ratings'].astype(int)

    # Menyimpan dataframe yang telah dibersihkan ke file CSV
    df.to_csv('/opt/airflow/data/P2M3_Valdi_data_clean.csv', index=False)
    print("-------Data Saved------")

# Function to post the data to Kibana
def post_to_kibana():
    es = Elasticsearch("http://elasticsearch:9200")
    df = pd.read_csv('/opt/airflow/data/P2M3_Valdi_data_clean.csv')
    
    for i, r in df.iterrows():
        doc = r.to_json()
        res = es.index(index="public.table_m3", id=i+1, body=doc)
        print(res)
