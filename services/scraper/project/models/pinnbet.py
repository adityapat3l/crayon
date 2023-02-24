import os
import requests
import datetime
from sqlalchemy import create_engine, text

from urls import PINNBET_BASE_FOOTBALL_URL
import json


engine = create_engine(os.getenv('DATABASE_URL'))
now = datetime.datetime.now()
DAYS = 90


def get_future_dates(days=90):
    """
    Number of days in the future we want a list for
    :param days: Number of days
    :return: yields List of dates
    """
    base = datetime.datetime.today()
    for d in range(days):
        yield base + datetime.timedelta(days=d+1)


def make_urls_to_request(base_url, days=90):
    """
    Combine a base_url with the number of days to look forward to create a URL that can used to request the data.
    :param base_url: found in the urls.py folder
    :param days: days to look forward
    :return: yields url to request
    """
    for dt in get_future_dates(days=days):
        str_day = str(dt.date())
        yield base_url + str_day


def run():
    base_url = PINNBET_BASE_FOOTBALL_URL
    days = DAYS
    for url in make_urls_to_request(base_url, days=days):
        with engine.begin() as cnx:
            pinnbet_data = requests.get(url).json()
            insert_stmt = text(f"""INSERT INTO pinnbet_raw (created_at, rec) VALUES (:now, :pinnbet_data)""")
            for game in pinnbet_data:
                cnx.execute(insert_stmt, {'now': now, 'pinnbet_data': json.dumps(game)})


if __name__ == '__main__':
    run()
