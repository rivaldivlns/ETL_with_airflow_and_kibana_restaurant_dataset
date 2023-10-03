'''
=================================================
Milestone 3

Name: Rivaldi Valensia
Batch: FTDS-007-HCK

Program ini dibuat untuk melakukan automatisasi transform dan load datamenggunakan PostgreSQL, Airflow dan Visualisasi menggunakan ElasticSearch& Kibana. 
Adapun dataset yang digunakan adalah dataset mengenai data restaurant.
=================================================
'''

-- Active: 1695467562253@@127.0.0.1@5432@db_phase2@public
-- Membuat database
-- CREATE DATABASE db_phase2
--     WITH
--     OWNER = airflow
--     ENCODING = 'UTF8'
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;
DROP TABLE public.table_M3;
--Membuat tabel
CREATE TABLE public.table_M3
(
    id INTEGER,
    area VARCHAR(255),
    city VARCHAR(255),
    restaurant VARCHAR(255),
    price FLOAT,
    "average_ratings" FLOAT,
    "total_ratings" INTEGER,
    "food_type" VARCHAR(255),
    address VARCHAR(255),
    "delivery_time" INTEGER,
    PRIMARY KEY (id)
);

--  COPY table_M3(
--     id,
--     area,
--     city,
--     restaurant,
--     price,
--     average_ratings,
--     total_ratings,
--     food_type,
--     address,
--     delivery_time
--  )

psql: \copy public.table_M3 FROM '/tmp/P2M3_Valdi_data_raw.csv' DELIMITER ',' CSV HEADER;

select * from public.table_M3
