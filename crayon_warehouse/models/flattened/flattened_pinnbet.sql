{{ config(materialized='table') }}


with subquery as (  select created_at                                  as rec_created_at,
                         rec::json ->> 'homeTeamName'                as home_team_name,
                         rec::json ->> 'awayTeamName'                as away_team_name,
                         rec::json ->> 'marketsCount'                as market_count,
                         (rec::json ->> 'eventId')::INT              as event_id,
                         (rec::json ->> 'roundId')::INT              as round_id,
                         rec::json ->> 'sportCode'                   as sport_code,
                         rec::json ->> 'eventStatus'                 as event_status,
                         rec::json ->> 'competitionId'               as competition_id,
                         (rec::json ->> 'matchStartTime')::TIMESTAMP as match_start_time,
                         sel::json ->> 'selectionCode' as selection_code,
                         sel::json ->> 'marketCode' as market_code,
                         sel::json ->> 'odds' as odd_value,
                         sel::json ->> 'result' as odd_result,
                         sel::json ->> 'status' as odd_status,
                         row_number() over (PARTITION BY rec::json->>'eventId',
                                    sel::json->>'selectionCode'
                       ORDER BY created_at::DATE DESC
                    ) as rank
                  from {{ source('raw_scrapes', 'pinnbet_raw') }} pr
                  cross join json_array_elements(pr.rec->'selections') as sel
)

select *,
      concat(event_id, '_', selection_code) as unique_id
from subquery
where rank = 1