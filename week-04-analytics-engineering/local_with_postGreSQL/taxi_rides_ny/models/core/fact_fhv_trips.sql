{{
    config(
        materialized='table'
    )
}}

with dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select fhvtrips.tripid, 
    fhvtrips.dispatching_base_num, 
    fhvtrips.sr_flag,
    fhvtrips.affiliated_base_number, 
    fhvtrips.pickup_locationid, 
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    fhvtrips.dropoff_locationid,
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    fhvtrips.pickup_datetime, 
    fhvtrips.dropoff_datetime
from {{ ref('stg_fhv_tripdata') }} as fhvtrips
inner join dim_zones as pickup_zone
on fhvtrips.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhvtrips.dropoff_locationid = dropoff_zone.locationid