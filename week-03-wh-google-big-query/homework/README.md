# Module 3 Homework

## GBQ (Google Big Query)

## Loading Parquet file to GCS
Using terraform [repository here](../gcp/main.tf):
```
# Upload a text file as an object to the storage bucket
resource "google_storage_bucket_object" "green_tripdata" {
 for_each =  toset(local.file_prefix)
 name         = "green_tripdata/tripdata_2022-${each.value}.parquet"
 source       = "./samples/green_tripdata_2022-${each.value}.parquet"
 content_type = "text/plain"
 bucket       = google_storage_bucket.bucket.id
}

```

## Create External table
Using terraform [repository here](../gcp/main.tf):
```
resource "google_bigquery_table" "green_tripdata" {
  dataset_id  = google_bigquery_dataset.dataset.dataset_id
  table_id    = "green_dataset"

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    ignore_unknown_values = true
    source_uris = [
      "gs://${var.gcs_bucket_name}/green_tripdata/*"
    ]
  }
}
```
##

## Create table
```sql
-- Create table from external table
CREATE OR REPLACE TABLE `zoomcamp_gbq_wk3.nyc_green_taxi` AS
SELECT * FROM `zoomcamp_gbq_wk3.green_dataset`;
```

## Question 1. 
### What is count of records for the 2022 Green Taxi Data??
- 840,402

```sql
SELECT COUNT(*) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.green_dataset` ;

-- OR

SELECT COUNT(*) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi` ;
```


## Question 2:
### Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. 
### What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
- 0 MB for the External Table and 6.41MB for the Materialized Table

```sql
-- On the External Table 
SELECT COUNT(DISTINCT PULocationID) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.green_dataset`

-- On the Table
SELECT COUNT(DISTINCT PULocationID) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi`
```

## Question 3:
### How many records have a fare_amount of 0? 
- 1,622

```sql
SELECT COUNT(*) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi` WHERE fare_amount = 0;
```

## Question 4:
### What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)
- Partition by lpep_pickup_datetime Cluster on PUlocationID
```sql
SELECT COUNT(*) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi` WHERE fare_amount = 0;

-- Create a new table with this strategy
CREATE OR REPLACE TABLE `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi_partitionned`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.green_dataset`;
```

# Question 5:
### Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)

### Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

### Choose the answer which most closely matches.
- 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table

```sql
-- Using the materialized table
SELECT distinct PULocationID 
FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi`
WHERE DATE(lpep_pickup_datetime) between DATE('2022-06-01') AND DATE('2022-06-30');

-- Using the partitioned table
SELECT distinct PULocationID 
FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi_partitionned`
WHERE DATE(lpep_pickup_datetime) between DATE('2022-06-01') AND DATE('2022-06-30');
```

# Question 6:
### Where is the data stored in the External Table you created?
- GCP Bucket

# Question 7:
### It is best practice in Big Query to always cluster your data:
- True

```
Clustering is basically the ordering of data within a partition. Making a cluster allows BigQuery to keep similar data conjointly and boost performance by scanning just a few records when a query is run. If clustering is used the right way it can provide many performance-related benefits.
````

# Question 8:
### It is best practice in Big Query to always cluster your data:
- 0 MB

```
Because Google Big Query stores metadata for each partition
```