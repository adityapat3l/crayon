from flask import Blueprint, jsonify, request
from project.models import pinnbet, maxbet
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
        pinnbet.run()
    elif website_name == 'maxbet':
        maxbet.run()
        
    return jsonify({"status": "success", "website": f"{website_name}"})
        
        