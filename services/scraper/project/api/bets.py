from flask import Blueprint, jsonify

bets_blueprint = Blueprint("bets", __name__, template_folder="./templates")


@bets_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify({"status": "success", "message": "pong!"})