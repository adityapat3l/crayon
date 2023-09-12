import requests
import logging

url = "http://crayon:5000"


def run_request():
    pinnbet_res = requests.post(f"{url}/run_scrapes", params={"website_name": "pinnbet"})
    maxbet_res = requests.post(f"{url}/run_scrapes", params={"website_name": "maxbet"})
    logging.info(pinnbet_res.text)
    logging.info(maxbet_res.text)
