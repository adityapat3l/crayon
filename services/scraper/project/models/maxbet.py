import os
import requests
import datetime
from sqlalchemy import create_engine, text
from urls import MAXBET_FOOTBALL
import json

# All sport leagues from maxbet

engine = create_engine(os.getenv('DATABASE_URL'))
now = datetime.datetime.now()


def run():
    url = MAXBET_FOOTBALL
    with engine.begin() as cnx:
        maxbet_data = requests.get(url).json()
        insert_stmt = text(f"""INSERT INTO maxbet_raw (created_at, rec) VALUES (:created_at, :maxbet_data)""")
        for game in maxbet_data:
            cnx.execute(insert_stmt, {'created_at': now, 'maxbet_data': json.dumps(game)})


if __name__ == '__main__':
    run()




# with engine.begin() as cnx:
#
#     for league in football_json:
#         league_id = league['betLeagueId']
#         league_code = league['leagueCode']
#         league_name = league['name']
#         sport = league['sport']
#         match_cnt = len(league['matchList'])
#         created_at = now_dt
#         scrape_site = 'MAXBET'
#
#         league_data = (league_id, league_code, league_name, sport, match_cnt, created_at, scrape_site)
#
#         league_insert_sql = text(f"""INSERT INTO dim_football_append (league_id, league_code, league_name, sport, match_cnt, created_at, scrape_site)
#                                       VALUES {league_data}"""
#         )
#
#         for match in league['matchList']:
#             match_id = match['id']
#             match_round = match['round']
#             league_id = match['leagueId']
#             team_home = match['home']
#             team_away = match['away']
#             team_home_id = match['homeId']
#             team_away_id = match['awayId']
#
#             kickoff_time_epoch = match['kickOffTime']
#             created_at = now_dt
#
#             for odd in match['odBetPickGroups']:
#                 odd_name = odd['name']
#                 odd_description = odd['description']
#
#                 for tip in odd['tipTypes']:
#                     tip_description = tip['description']
#                     tip_value = tip['value']
#
#                     odd_data = {'match_id': match_id,
#                                 'match_round': match_round,
#                                 'league_id': league_id,
#                                 'team_home': team_home,
#                                 'team_away': team_away,
#                                 'team_home_id': team_home_id,
#                                 'team_away_id': team_away_id,
#                                 'kickoff_time_epoch': kickoff_time_epoch,
#                                 'odd_name': odd_name,
#                                 'odd_description': odd_description,
#                                 'tip_description': tip_description,
#                                 'tip_value': tip_value,
#                                 'created_at': created_at,
#                                 'scrape_site': scrape_site
#                                 }
#
#                     odd_insert_sql = text("""
#                     INSERT INTO fact_football_append (match_id, match_round, league_id, team_home, team_away,
#                                                     team_home_id, team_away_id,  kickoff_time_epoch, odd_name,
#                                                     odd_description, tip_description, tip_value, created_at, scrape_site)
#                                            VALUES (:match_id,
#                                                    :match_round,
#                                                    :league_id,
#                                                    :team_home,
#                                                    :team_away,
#                                                    :team_home_id,
#                                                    :team_away_id,
#                                                    :kickoff_time_epoch,
#                                                    :odd_name,
#                                                    :odd_description,
#                                                    :tip_description,
#                                                    :tip_value,
#                                                    :created_at,
#                                                    :scrape_site) """)
#                     cnx.execute(odd_insert_sql, odd_data)
#
#         cnx.execute(league_insert_sql)
