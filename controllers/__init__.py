
from .UsuarioController import usuario_blueprint
from .PropostaController import proposta_blueprint

blueprints = [
    (usuario_blueprint, "/api/usuario"),
    (proposta_blueprint, "/api/proposta")
]
