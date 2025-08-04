
from .UsuarioController import usuario_blueprint
from .PropostaController import proposta_blueprint
from .FornecedorController import fornecedor_blueprint
from .LicitacaoController import licitacao_blueprint

blueprints = [
    (usuario_blueprint, "/api/usuario"),
    (proposta_blueprint, "/api/proposta"),
    (fornecedor_blueprint, "/api/fornecedor"),
    (licitacao_blueprint, "/api/licitacao")
]
