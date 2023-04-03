from flask import Blueprint, jsonify, request
from project.api import fetch_maxbet, fetch_pinnbet
import logging

bets_blueprint = Blueprint("bets", __name__, template_folder="./templates")


@bets_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify({"status": "success", "message": "pong!"})


@bets_blueprint.route("/run_scrapes", methods=["POST"])
def run_scrapes():
    website_name = request.args.get('website_name')
    print(website_name)
    logging.info(str(website_name))
    
    if website_name == 'pinnbet':
        fetch_pinnbet.run()
    elif website_name == 'maxbet':
        fetch_maxbet.run()
        
    return jsonify({"status": "success", "website": f"{website_name}"})
        
        