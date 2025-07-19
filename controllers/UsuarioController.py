from flask import Blueprint, request,render_template,redirect, url_for, flash, session
from services import UsuarioService as _service

usuario_blueprint = Blueprint("usuario", __name__)

@usuario_blueprint.route("/cadastrar", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return {"erro": "Email e senha são obrigatórios."}, 400

    return _service.cadastrar_usuario(email, senha)

@usuario_blueprint.route("/login", methods=["POST"])
def login_usuario():
    email = request.form.get("email") or request.form.get("username")
    senha = request.form.get("senha") or request.form.get("password")

    if not email or not senha:
        flash("Email e senha são obrigatórios.", "error")
        return redirect(url_for("usuario.tela_login"))  

    try:
        dados = _service.login(email, senha)
        session['idToken'] = dados['idToken']
        session['refreshToken'] = dados['refreshToken']
        session['uid'] = dados['localId']
        session['email'] = dados['email']

        return redirect(url_for("usuario.tela_home"))  
    except ValueError as e:
        flash("Email ou Senha incorretos", "error")
        return redirect(url_for("usuario.tela_login"))  


@usuario_blueprint.route("/index", methods=["GET"])
def tela_login():
    return render_template("index.html")

@usuario_blueprint.route("/home", methods=["GET"])
def tela_home():
    return render_template("home.html")
