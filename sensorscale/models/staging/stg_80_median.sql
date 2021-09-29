{{ config(materialized='view') }}
with source as (

    select * from {{ ref('I80_median')}} 
),

stage_median as (

    select 

        ID,
        weekday,
        hour,
        minute,
        Second,
        flow1,
        occupancy1,
        mph1,
        flow2,
        occupancy2,
        mph2,
        flow3,
        occupancy3,
        mph3,
        flow4,
        occupancy4,
        mph4,
        flow5,
        occupancy5,
        mph5,
        totalflow

    from source

)

select * from stage_median