import os
from flask import Blueprint, jsonify, render_template, request
from models.Fornecedor import Fornecedor as FornecedorMapper
from services import FornecedorService as _service

fornecedor_blueprint = Blueprint("fornecedor", __name__)

@fornecedor_blueprint.route("/cadastrar", methods=["POST"])
def cadastrar_fornecedor():
    try:
        data = request.form.to_dict()
        arquivo = request.files.get("logomarca")
        pasta_destino = os.path.join("static", "logomarca", data.get("razao_social"))
        caminho_logomarca = os.path.join("logomarca", data.get("razao_social"))
        os.makedirs(pasta_destino, exist_ok=True)  
        caminho_arquivo = os.path.join(pasta_destino, arquivo.filename)
        arquivo.save(caminho_arquivo)
        data["caminho_logomarca"] = caminho_logomarca.replace("\\", "/")
        data["nome_logomarca"] = arquivo.filename      
        _service.cadastrar_fornecedor(data)
        
        resultado = {
            "mensagem": "Licitação cadastrada com sucesso!"
        }
        return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@fornecedor_blueprint.route("/listar", methods=["GET"])
def listar_fornecedores():
    fornecedores = _service.listar_fornecedores()
    return jsonify([f.to_json() for f in fornecedores])
