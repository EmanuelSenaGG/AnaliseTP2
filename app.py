from flask import Flask, render_template
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
    app.secret_key = "19042002" 
    app.config["ApiGeminiKey"] = "SUA KEY AQUI"
    app.config["FIREBASE_DB"] = db
    app.config["FIREBASE_AUTH"] = auth
    app.json.dumps = lambda obj, **kwargs: json.dumps(obj, ensure_ascii=False, **kwargs)

    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)


    @app.route('/')
    def raiz():
        return render_template('index.html') 
     
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
