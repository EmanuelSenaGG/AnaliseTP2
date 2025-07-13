from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, auth
from controllers import blueprints
import json

def create_app():
    cred = credentials.Certificate("config/firebase-key.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    app = Flask(__name__)
    app.config["FIREBASE_DB"] = db
    app.config["FIREBASE_AUTH"] = auth
    app.json.dumps = lambda obj, **kwargs: json.dumps(obj, ensure_ascii=False, **kwargs)

    @app.route('/')
    def raiz():
        return jsonify({"mensagem": "Bem-vindo à API!"})  

    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
