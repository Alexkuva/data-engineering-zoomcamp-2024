## Week 5 Homework

## Question 1. Install Spark and PySpark
### Execute spark.version. What's the output?
- `--rm`

## Question 2.
### What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.
- 0.42.0

## Question 3. Count records
### How many taxi trips were there on the 15th of October?
- 15612
```SQL
SELECT count(*)
FROM yellow_taxi_trips
WHERE DATE(lpep_pickup_datetime) = '2019-09-18'
AND DATE(lpep_dropoff_datetime) = '2019-09-18';
```

## Question 4. Largest trip for each day
### Longest trip for each day
- 2019-09-26
```SQL
SELECT DATE(lpep_pickup_datetime)
FROM yellow_taxi_trips
WHERE trip_distance = (SELECT max(trip_distance) FROM yellow_taxi_trips);
```

## Question 5. User Interface
### Spark’s User Interface which shows the application's dashboard runs on which local port?
- "Brooklyn" "Manhattan" "Queens"
```SQL
SELECT z."Borough"
FROM yellow_taxi_trips y
JOIN taxi_zone z ON y."PULocationID" = z."LocationID"
WHERE DATE(y.lpep_pickup_datetime) = '2019-09-18'
AND z."Borough" <> 'Unknown'
GROUP BY z."Borough"
HAVING SUM(y.total_amount) > 50000
ORDER BY SUM(y.total_amount) DESC
```

## Question 6. Least frequent pickup location zone
### Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?
- JFK Airport
```SQL
SELECT en."Zone", MAX(y.tip_amount)
FROM yellow_taxi_trips y
JOIN taxi_zone st ON y."PULocationID" = st."LocationID"
JOIN taxi_zone en ON y."DOLocationID" = en."LocationID"
WHERE EXTRACT(MONTH FROM DATE(y.lpep_pickup_datetime)) = 9
AND EXTRACT(YEAR FROM DATE(y.lpep_pickup_datetime)) = 2019
AND st."Zone" = 'Astoria'
GROUP BY en."Zone"
ORDER BY max(y.tip_amount) DESC
LIMIT 1
```