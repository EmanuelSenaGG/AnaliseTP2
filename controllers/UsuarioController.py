from flask import Blueprint, request,render_template,redirect, url_for, flash, session
from services import UsuarioService as _usuarioService
from services import FornecedorService as _fornecedorService
from services import LicitacaoService as _licitacaoService

login_admin = "admin"
senha_admin = "admin"
usuario_blueprint = Blueprint("usuario", __name__)



@usuario_blueprint.route("/login", methods=["POST"])
def login_usuario():
    login = request.form.get("login") or request.form.get("username")
    senha = request.form.get("senha") or request.form.get("password")

    if not login or not senha:
        flash("Login e senha são obrigatórios.", "error")
        return redirect(url_for("usuario.tela_login"))  

    if login == login_admin and senha == senha_admin:
        return redirect(url_for("usuario.tela_admin"))
    try:
        id = _usuarioService.login(login, senha)
        session['idFornecedor'] = id
        return redirect(url_for("usuario.tela_home"))  
    except ValueError as e:
        flash("Login ou Senha incorretos", "error")
        return redirect(url_for("usuario.tela_login"))  


@usuario_blueprint.route("/index", methods=["GET"])
def tela_login():
    return render_template("index.html")

@usuario_blueprint.route("/home", methods=["GET"])
def tela_home():
    try:
        licitacoes = _licitacaoService.listar_licitacoes_fornecedor(session.get('idFornecedor'))
        return render_template("home.html", licitacoes=licitacoes)
    except Exception as e:
        return f"Erro ao carregar fornecedores: {e}", 500


@usuario_blueprint.route("/telaadmin", methods=["GET"])
def tela_admin():
    try:
        fornecedores = _fornecedorService.listar_fornecedores()
        licitacoes = _licitacaoService.listar_licitacoes()
        return render_template("admin.html", fornecedores=fornecedores, licitacoes=licitacoes)
    except Exception as e:
        return f"Erro ao carregar fornecedores: {e}", 500