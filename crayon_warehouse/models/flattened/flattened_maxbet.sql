
{{ config(materialized='table') }}


with subquery as (
 select 
    created_at as rec_created_at,
    (rec::json->>'betLeagueId')::INT as bet_league_id,
    rec::json->>'name' as bet_league_name,
    rec::json->>'sport' as bet_league_sport,
    mat::json->>'id' as match_id,
    mat::json->>'round' as match_round,
    mat::json->>'matchCode' as match_code,
    mat::json->>'home' as match_home,
    mat::json->>'away' as match_away,
    to_timestamp((mat::json->>'kickOffTime')::NUMERIC / 1000)::TIMESTAMP as match_kickoff_time_utc,
    (mat::json->>'haveOdds')::BOOLEAN as has_match_odds,
    odds::json->>'id' as odds_id,
    odds::json->>'name' as odds_name,
    tips::json->>'tipTypeId' as tip_id,
    tips::json->>'tipType' as tip_type,
    tips::json->>'description' as tip_description,
    tips::json->>'value' as tip_value,
    row_number() over (PARTITION BY rec::json->>'betLeagueId',
                                    mat::json->>'id',
                                    odds::json->>'id',
                                    tips::json->>'tipTypeId'
                       ORDER BY created_at::DATE DESC
                    ) as rank
 from {{ source('raw_scrapes', 'maxbet_raw') }} as mr
 cross join json_array_elements(mr.rec->'matchList') as mat
 cross join json_array_elements(mat->'odBetPickGroups') as odds
 cross join json_array_elements(odds->'tipTypes') as tips
)

select
    concat(match_id, '_', tip_id) as unique_id,
    *
from subquery
where rank = 1
