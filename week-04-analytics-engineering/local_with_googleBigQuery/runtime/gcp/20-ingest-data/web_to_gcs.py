import io
import os
import requests
import datetime
from dateutil.relativedelta import *
import pandas as pd
from google.cloud import storage
from dotenv import load_dotenv
from pathlib import Path

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage python-dotenv`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# Load environment variables

load_dotenv()

print("Launching import service...")
prefix_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET")
print(f"Bucket is: {BUCKET}")


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(starting_date, ending_date, service):
    print(f"Starting Service : {service}")
    start = datetime.datetime.strptime(starting_date, '%Y%m')
    end = datetime.datetime.strptime(ending_date, '%Y%m')
    step = relativedelta(months=+1)

    while start <= end: 
        # sets the month part of the file_name string
        month_file=start.date().strftime("%Y-%m")
        print(f"Starting for {service}_tripdata_{month_file}.csv.gz ")

        # csv file_name
        file_name = f"{service}_tripdata_{month_file}.csv.gz"

        # download it using requests via a pandas df
        request_url = f"{prefix_url}{service}/{file_name}"
        r = requests.get(request_url)
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")

        # define type
        if service == "green":
            print("Using lpep_pickup_datetime as parse_dates.")
            taxi_dtypes = {
                        'VendorID': pd.Int64Dtype(),
                        'passenger_count': pd.Int64Dtype(),
                        'trip_distance': float,
                        'RatecodeID':pd.Int64Dtype(),
                        'store_and_fwd_flag':str,
                        'PULocationID':pd.Int64Dtype(),
                        'DOLocationID':pd.Int64Dtype(),
                        'payment_type': pd.Int64Dtype(),
                        'fare_amount': float,
                        'extra':float,
                        'mta_tax':float,
                        'tip_amount':float,
                        'tolls_amount':float,
                        'improvement_surcharge':float,
                        'total_amount':float,
                        'congestion_surcharge':float,
                        'trip_type': pd.Int64Dtype(),
                        'lpep_pickup_datetime': str,
                        'lpep_dropoff_datetime': str
                    }
        if service == "yellow":
            print("Using tpep_pickup_datetime as parse_dates.")
            taxi_dtypes = {
                        'VendorID': pd.Int64Dtype(),
                        'passenger_count': pd.Int64Dtype(),
                        'trip_distance': float,
                        'RatecodeID':pd.Int64Dtype(),
                        'store_and_fwd_flag':str,
                        'PULocationID':pd.Int64Dtype(),
                        'DOLocationID':pd.Int64Dtype(),
                        'payment_type': pd.Int64Dtype(),
                        'fare_amount': float,
                        'extra':float,
                        'mta_tax':float,
                        'tip_amount':float,
                        'tolls_amount':float,
                        'improvement_surcharge':float,
                        'total_amount':float,
                        'congestion_surcharge':float,
                        'tpep_pickup_datetime': str,
                        'tpep_dropoff_datetime': str
                    }
        if service == "fhv":
            print("Using pickup_datetime as parse_dates.")
            taxi_dtypes = {
                        'dispatching_base_num': str,
                        'PUlocationID':pd.Int64Dtype(),
                        'DOlocationID':pd.Int64Dtype(),
                        'SR_Flag': pd.Int64Dtype(),
                        'Affiliated_base_number': str,
                        'pickup_datetime': str,
                        'dropOff_datetime': str
                    }

        # read it back into a parquet file
        df = pd.read_csv(file_name, compression='gzip', dtype=taxi_dtypes)
        file_name = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(file_name, engine='pyarrow')
        print(f"Parquet: {file_name}")

        # upload it to gcs 
        upload_to_gcs(BUCKET, f"{service}__tripdata/{file_name}", file_name)
        print(f"GCS: {service}_tripdata/{file_name}")

        # add 1 month
        start += step

#services = ['fhv','green','yellow']
services = ['fhv']
starting_date = "201901"
ending_date = "201912"

print("Starting upload ...")
for service in services:
    web_to_gcs(starting_date, ending_date, service)