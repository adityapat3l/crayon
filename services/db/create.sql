--PINNBET
CREATE TABLE pinnbet_raw (
    created_at TIMESTAMP,
	rec json
);




CREATE TABLE IF NOT EXISTS dim_football_append (
league_id INT,
league_code INT,
league_name VARCHAR,
sport VARCHAR,
match_cnt INT,
created_at TIMESTAMP,
scrape_site VARCHAR
)
;

CREATE TABLE IF NOT EXISTS fact_football_append (
match_id INT,
match_round INT,
league_id VARCHAR,
team_home_id INT,
team_away_id INT,
team_home VARCHAR,
team_away VARCHAR,
kickoff_time_epoch BIGINT,

odd_name VARCHAR,
odd_description VARCHAR,
tip_description VARCHAR,
tip_value NUMERIC(38, 2),

created_at TIMESTAMP,
scrape_site VARCHAR
)
;