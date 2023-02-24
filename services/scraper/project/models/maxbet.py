import os

from bs4 import BeautifulSoup
import requests
# import pandas as pd
# from sqlalchemy import create_engine
from config import POSTGRES_URL

from urllib.parse import quote
import datetime
from sqlalchemy import create_engine, text

# All sport leagues from maxbeta
MAXBET_FOOTBALL = 'https://www.maxbet.rs/ibet/offer/leagues//-1/0.json?v=4.50.35.4&locale=en&token=152506%23117827%23117683%23117689%23132001%' \
'23117709%23130834%23124942%23134676%23185898%23132134%23169337%23152565%23132125%23176655%23168450%23160317%23186311%23146649%' \
'23157183%23138547%23133789%23170887%23134715%23119676%23132149%23119606%23117668%23117669%23137386%23137387%23137388%23139668%' \
'23139667%23152349%23152350%23134172%23142836%23182195%23142528%23117861%23117751%23175249%23152556%23132131%23133726%23133866%' \
'23140666%23149849%23117863%23117690%23143679%23143680%23143681%23176679%23146161%23178094%23176625%23132139%23169393%23152558%' \
'23182116%23169438%23132192%23167588%23132459%23117808%23132128%23174497%23169547%23132736%23132737%23175171%23176978%23167649%' \
'23130582%23117675%23122647%23122648%23122649%23152511%23167472%23117710%23124463%23124586%23178186%23178211%23178193%23178194%' \
'23178202%23181728%23182032%23181560%23181557%23181558%23181563%23181783%23181782%23181561%23181559%23181780%23182033%23181781%2' \
'3181564%23175332%23169437%23174513%23119607%23132133%23166115%23166116%23169334%23180714%23180715%23172071%23132145&ttgIds='

CREATE_DIM_TABLE = """
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
"""

CREATE_FACT_TABLE = """
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
"""

# All sport leagues from maxbet
football_json = requests.get(MAXBET_FOOTBALL).json()
engine = create_engine(os.getenv('DATABASE_URL'))

now_dt = str(datetime.datetime.now())

with engine.begin() as cnx:
    cnx.execute(text(CREATE_DIM_TABLE))
    cnx.execute(text(CREATE_FACT_TABLE))

with engine.begin() as cnx:

    for league in football_json:
        league_id = league['betLeagueId']
        league_code = league['leagueCode']
        league_name = league['name']
        sport = league['sport']
        match_cnt = len(league['matchList'])
        created_at = now_dt
        scrape_site = 'MAXBET'

        league_data = (league_id, league_code, league_name, sport, match_cnt, created_at, scrape_site)

        league_insert_sql = text(f"""INSERT INTO dim_football_append (league_id, league_code, league_name, sport, match_cnt, created_at, scrape_site) 
                                      VALUES {league_data}"""
        )

        for match in league['matchList']:
            match_id = match['id']
            match_round = match['round']
            league_id = match['leagueId']
            team_home = match['home']
            team_away = match['away']
            team_home_id = match['homeId']
            team_away_id = match['awayId']

            kickoff_time_epoch = match['kickOffTime']
            created_at = now_dt

            for odd in match['odBetPickGroups']:
                odd_name = odd['name']
                odd_description = odd['description']

                for tip in odd['tipTypes']:
                    tip_description = tip['description']
                    tip_value = tip['value']

                    odd_data = {'match_id': match_id,
                                'match_round': match_round,
                                'league_id': league_id,
                                'team_home': team_home,
                                'team_away': team_away,
                                'team_home_id': team_home_id,
                                'team_away_id': team_away_id,
                                'kickoff_time_epoch': kickoff_time_epoch,
                                'odd_name': odd_name,
                                'odd_description': odd_description,
                                'tip_description': tip_description,
                                'tip_value': tip_value,
                                'created_at': created_at,
                                'scrape_site': scrape_site
                                }

                    odd_insert_sql = text("""
                    INSERT INTO fact_football_append (match_id, match_round, league_id, team_home, team_away,
                                                    team_home_id, team_away_id,  kickoff_time_epoch, odd_name, 
                                                    odd_description, tip_description, tip_value, created_at, scrape_site) 
                                           VALUES (:match_id, 
                                                   :match_round, 
                                                   :league_id, 
                                                   :team_home, 
                                                   :team_away,
                                                   :team_home_id,
                                                   :team_away_id,  
                                                   :kickoff_time_epoch, 
                                                   :odd_name, 
                                                   :odd_description,
                                                   :tip_description, 
                                                   :tip_value,
                                                   :created_at,
                                                   :scrape_site) """)
                    cnx.execute(odd_insert_sql, odd_data)

        cnx.execute(league_insert_sql)
