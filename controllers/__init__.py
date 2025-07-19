
from .UsuarioController import usuario_blueprint

blueprints = [
    (usuario_blueprint, "/api/usuario")
]
