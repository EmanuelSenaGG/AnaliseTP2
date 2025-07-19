from flask import jsonify, current_app
import requests

FIREBASE_API_KEY = "AIzaSyAec6kanhA1T-GYkpwgxP7xIOKemRatXYI"  
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

def cadastrar_usuario(email,senha):
    try:
        auth = current_app.config["FIREBASE_AUTH"]
        user = auth.create_user(email=email, password=senha)
        return jsonify({
            "mensagem": "Usuário criado com sucesso!",
            "uid": user.uid,
            "email": user.email
        }), 201
    except:
        raise


def login(email, senha):
    payload = {
        "email": email,
        "password": senha,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()  
    else:
        erro = response.json()
        raise ValueError(erro.get("error", {}).get("message", "Erro desconhecido"))
