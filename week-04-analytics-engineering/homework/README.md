# Module 4 Homework

## DBT (Data Build Tool)

## Question 1:
### What happens when we execute dbt build --vars '{'is_test_run':'true'}'
- It applies a limit 100 only to our staging models

Only in stg_green_tripdata.sql, stg_yellow_tripdata.sql & stg_fhv_tripdata.
```sql
-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
```


## Question 2:
### What is the code that our CI job will run? Where is this code coming from?
- The code from a development branch requesting a merge to main


## Question 3:
### What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)?
- 22 998 722 (~23M)

```
dbt build --select stg_green_tripdata --vars '{'is_test_run':'false'}'
dbt build --select stg_yellow_tripdata --vars '{'is_test_run':'false'}'
dbt build --select stg_fhv_tripdata --vars '{'is_test_run':'false'}'
dbt build --vars '{'is_test_run':'false'}'
```

## Question 4:
### What is the service that had the most rides during the month of July 2019 month with the biggest amount of rides after building a tile for the fact_fhv_trips table?
- Yellow