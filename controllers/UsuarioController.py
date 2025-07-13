from flask import Blueprint, jsonify, request, current_app
import requests

FIREBASE_API_KEY = "AIzaSyAec6kanhA1T-GYkpwgxP7xIOKemRatXYI"  
usuario_blueprint = Blueprint("usuario", __name__)

@usuario_blueprint.route("/cadastrar", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    try:
        auth = current_app.config["FIREBASE_AUTH"]
        user = auth.create_user(email=email, password=senha)
        return jsonify({
            "mensagem": "Usuário criado com sucesso!",
            "uid": user.uid,
            "email": user.email
        }), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@usuario_blueprint.route("/login", methods=["POST"])
def login_usuario():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

    payload = {
        "email": email,
        "password": senha,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        resp_data = response.json()
        return jsonify({
            "mensagem": "Login realizado com sucesso!",
            "idToken": resp_data["idToken"],
            "refreshToken": resp_data["refreshToken"],
            "uid": resp_data["localId"],
            "email": resp_data["email"]
        })
    else:
        erro = response.json()
        return jsonify({"erro": erro.get("error", {}).get("message", "Erro desconhecido")}), 401

