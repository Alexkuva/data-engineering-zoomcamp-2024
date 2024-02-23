#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time
import datetime
from dateutil.relativedelta import *

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    schema = params.schema
    table_name = params.table_name
    prefix_url = params.url
    starting_date =  params.starting_date
    ending_date =  params.ending_date
    is_test_run = params.is_test_run

    start = datetime.datetime.strptime(starting_date, '%Y%m')
    end = datetime.datetime.strptime(ending_date, '%Y%m')
    step = relativedelta(months=+1)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    while start <= end: 
        month_file=start.date().strftime("%Y-%m")
        print(f"Start : {month_file}")
        url = prefix_url + '_'+ month_file + '.csv.gz'
        # the backup files are gzipped, and it's important to keep the correct extension
        # for pandas to be able to open the file
        if url.endswith('.csv.gz'):
            csv_name = 'output.csv.gz'
        else:
            csv_name = 'output.csv'

        os.system(f"wget {url} -O {csv_name}")

        print(f"OUTPUT = {os.system(f'stat {csv_name}')}")

        print("Read csv file.")
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=10000)

        print("Starting first iterator.")
        df = next(df_iter)

        if "lpep_pickup_datetime" in df.columns:
            print(f"Using lpep_pickup_datetime before df.head")
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        if "tpep_pickup_datetime" in df.columns:
            print(f"Using tpep_pickup_datetime before df.head")
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        if "pickup_datetime" in df.columns:
            print(f"Using tpep_pickup_datetime before df.head")
            df.pickup_datetime = pd.to_datetime(df.pickup_datetime)
            df.pickup_datetime = pd.to_datetime(df.pickup_datetime)

        df.head(n=0).to_sql(name=table_name, schema=schema, con=engine, if_exists='replace')

        df.to_sql(name=table_name, schema=schema, con=engine, if_exists='append')

        if not is_test_run:
            while True: 

                try:
                    t_start = time()
                    
                    df = next(df_iter)
                    
                    if "lpep_pickup_datetime" in df.columns:
                        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
                        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

                    if "tpep_pickup_datetime" in df.columns:
                        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
                        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

                    if "pickup_datetime" in df.columns:
                        df.pickup_datetime = pd.to_datetime(df.pickup_datetime)
                        df.pickup_datetime = pd.to_datetime(df.pickup_datetime)

                    df.to_sql(name=table_name, schema=schema, con=engine, if_exists='append')

                    t_end = time()

                    print('inserted another chunk, took %.3f second' % (t_end - t_start))

                except StopIteration:
                    print("Finished ingesting data into the postgres database")
                    break
            # add 1 month
            start += step

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--schema', required=True, help='schema name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')
    parser.add_argument('--starting_date', required=True, help='first date to upload from the url')
    parser.add_argument('--ending_date', required=True, help='last date to upload from the url')
    parser.add_argument('--is_test_run', required=True, help='if true load sample data')

    args = parser.parse_args()

    main(args)