-- Create table from external table
CREATE OR REPLACE TABLE `zoomcamp_gbq_wk3.nyc_green_taxi` AS
SELECT * FROM `zoomcamp_gbq_wk3.green_dataset`;


-- Question 1. : What is count of records for the 2022 Green Taxi Data??
SELECT COUNT(*) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.green_dataset` ;
-- OR
SELECT COUNT(*) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi` ;


-- Question 2. :  Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. 
-- On the External Table 
SELECT COUNT(DISTINCT PULocationID) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.green_dataset`
-- On the Table
SELECT COUNT(DISTINCT PULocationID) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi`


-- Question 3: How many records have a fare_amount of 0? 
SELECT COUNT(*) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi` WHERE fare_amount = 0;

-- Question 4: What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)
SELECT COUNT(*) FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi` WHERE fare_amount = 0;

-- Create a new table with this strategy
CREATE OR REPLACE TABLE `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi_partitionned`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.green_dataset`;


-- Question 5: Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
-- Using the materialized table
SELECT distinct PULocationID 
FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi`
WHERE DATE(lpep_pickup_datetime) between DATE('2022-06-01') AND DATE('2022-06-30');
-- Using the partitioned table
SELECT distinct PULocationID 
FROM `onyx-hangout-411709.zoomcamp_gbq_wk3.nyc_green_taxi_partitionned`
WHERE DATE(lpep_pickup_datetime) between DATE('2022-06-01') AND DATE('2022-06-30');