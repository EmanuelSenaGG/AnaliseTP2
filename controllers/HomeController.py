from flask import Blueprint, jsonify, request


home_blueprint = Blueprint("api", __name__)

@home_blueprint.route("/", methods=["GET"])
def index():
    return jsonify({"mensagem": "API Flask modularizada!"})


