import os
import requests
import datetime
from sqlalchemy import create_engine, text

from .urls import PINNBET_BASE_FOOTBALL_URL
import json


DAYS = 14
engine = create_engine(os.getenv('DATABASE_URL'))

def make_url_to_request(base_url, days=90):
    """
    Combine a base_url with the number of days to look forward to create a URL that can used to request the data.
    :param base_url: found in the urls.py folder
    :param days: days to look forward
    :return: yields url to request
    """

    add_days = datetime.datetime.today() + datetime.timedelta(days=days)
    return base_url + str(add_days)


def run(engine=engine):
    now = datetime.datetime.now()
    base_url = PINNBET_BASE_FOOTBALL_URL
    days = DAYS
    url = make_url_to_request(base_url, days=days)
    with engine.begin() as cnx:
        pinnbet_data = requests.get(url).json()
        insert_stmt = text(f"""INSERT INTO pinnbet_raw (created_at, rec) VALUES (:created_at, :pinnbet_data)""")
        for game in pinnbet_data:
            cnx.execute(insert_stmt, {'created_at': now, 'pinnbet_data': json.dumps(game)})


if __name__ == '__main__':
    run(engine=engine)
