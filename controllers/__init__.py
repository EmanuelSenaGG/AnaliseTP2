
from .HomeController import home_blueprint
from .UsuarioController import usuario_blueprint

blueprints = [
    (home_blueprint, "/api/home"),
    (usuario_blueprint, "/api/usuario")
]
