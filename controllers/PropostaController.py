
from flask import Blueprint, jsonify, render_template, request, session
from services import PropostaService as _serviceProposta
from services import LicitacaoService as _licitacaoService
from services import FornecedorService as _serviceFornecedor

proposta_blueprint = Blueprint("proposta", __name__)

@proposta_blueprint.route("/carregar_proposta/<idLicitacao>", methods=["GET"])
def carregar_proposta(idLicitacao):
    try:
        licitacao = _licitacaoService.obter_licitacao_por_id(idLicitacao)
        fornecedor =  _serviceFornecedor.obter_fornecedor_por_id(session.get('idFornecedor'))
        return render_template("proposta.html", licitacao=licitacao, fornecedor=fornecedor)
    except Exception as e:
        return {"erro": str(e)}, 500


@proposta_blueprint.route("/gerar_proposta/<path:idLicitacao>", methods=["GET"])
def gerar_proposta(idLicitacao):
    caminho_arquivo = _licitacaoService.obter_path_arquivo_licitacao_por_id(idLicitacao)
    resultado = _serviceProposta.analisar_pdf(caminho_arquivo)
    json = jsonify(resultado)
    return json


@proposta_blueprint.route("/gerar_html_proposta", methods=["POST"])
def gerar_html_proposta():
    try:
        dados = request.get_json()
        return _serviceProposta.gerar_html_proposta(dados)
     
    except Exception as e:
        return {"erro": str(e)}, 500
    
