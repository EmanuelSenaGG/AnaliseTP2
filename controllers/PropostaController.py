from flask import Blueprint, request
from services import PropostaService as _service



proposta_blueprint = Blueprint("proposta", __name__)

@proposta_blueprint.route("/gerar", methods=["POST"])
def gerar_proposta():
    data = request.get_json()
    html_gerado = _service.gerar_pdf(data)
    return html_gerado, 200, {"Content-Type": "text/html; charset=utf-8"}

  
    
