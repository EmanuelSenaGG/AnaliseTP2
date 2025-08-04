from flask import Blueprint, jsonify, request, send_from_directory,current_app
from services import LicitacaoService as _licitacao_service
import os

licitacao_blueprint = Blueprint("licitacao", __name__)


@licitacao_blueprint.route("/cadastrar", methods=["POST"])
def cadastrar_licitacao():
    try:
        data = request.form.to_dict()
        arquivo = request.files.get("arquivo")
        pasta_destino = os.path.join("uploads", data.get("empresa"))
        os.makedirs(pasta_destino, exist_ok=True)  
        caminho_arquivo = os.path.join(pasta_destino, arquivo.filename)
        arquivo.save(caminho_arquivo)
        data["caminho_arquivo"] = caminho_arquivo 
        data["nome_arquivo"] = arquivo.filename  
        _licitacao_service.cadastrar_licitacao(data)
        return jsonify({"mensagem": "Licitação cadastrada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@licitacao_blueprint.route("/listar", methods=["GET"])
def listar_licitacoes():
    licitacoes = _licitacao_service.listar_licitacoes()
    return jsonify([l.to_json() for l in licitacoes])


@licitacao_blueprint.route("/registrarvinculos", methods=["POST"])
def vincular_fornecedores():
    try:
        dados = request.get_json()
        licitacao_id = dados.get('licitacao_id')
        fornecedores = dados.get('fornecedores')  
        _licitacao_service.registrar_vinculos(licitacao_id, fornecedores)
        return jsonify({"mensagem": "Vínculo realizado com sucesso"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
   

@licitacao_blueprint.route('/uploads/<path:pathArquivo>')
def obter_arquivo(pathArquivo):
    pasta_uploads = os.path.join(current_app.root_path, 'uploads')
    diretorio = os.path.dirname(pathArquivo)
    arquivo = os.path.basename(pathArquivo)
    caminho_completo = os.path.join(pasta_uploads, diretorio)
    try:
        return send_from_directory(caminho_completo, arquivo)
    except FileNotFoundError:
        os.abort(404, description="Arquivo não encontrado")

    