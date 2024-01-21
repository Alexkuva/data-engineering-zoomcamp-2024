## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL

## Question 1. Knowing docker tags
- `--rm`

## Question 2. Understanding docker first run 
- 0.42.0

## Question 3. Count records
- 15612
```SQL
SELECT count(*)
FROM yellow_taxi_trips
WHERE DATE(lpep_pickup_datetime) = '2019-09-18'
AND DATE(lpep_dropoff_datetime) = '2019-09-18';
```

## Question 4. Largest trip for each day
- 2019-09-26
```SQL
SELECT DATE(lpep_pickup_datetime)
FROM yellow_taxi_trips
WHERE trip_distance = (SELECT max(trip_distance) FROM yellow_taxi_trips);
```

## Question 5. Three biggest pick up Boroughs
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

## Question 6. Largest tip
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

## Question 7. Creating Resources
```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "zoomcamp_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "onyx-hangout-411709"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-zoomcamp_wk1"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: 
```