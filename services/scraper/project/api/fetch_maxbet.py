import os
import requests
import datetime
from sqlalchemy import create_engine, text
from project.api.urls import MAXBET_FOOTBALL
import json

# All sport leagues from maxbet
engine = create_engine(os.getenv('DATABASE_URL'))

def run(engine=engine):
    now = datetime.datetime.now()
    url = MAXBET_FOOTBALL
    with engine.begin() as cnx:
        maxbet_data = requests.get(url).json()
        insert_stmt = text(f"""INSERT INTO maxbet_raw (created_at, rec) VALUES (:created_at, :maxbet_data)""")
        for game in maxbet_data:
            cnx.execute(insert_stmt, {'created_at': now, 'maxbet_data': json.dumps(game)})


if __name__ == '__main__':
    run(engine=engine)