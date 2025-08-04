from flask import jsonify, current_app
from models.Fornecedor import Fornecedor as FornecedorMapper


FIREBASE_API_KEY = "AIzaSyAec6kanhA1T-GYkpwgxP7xIOKemRatXYI"  
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

def cadastrar_usuario(email,senha):
    try:
        auth = current_app.config["FIREBASE_AUTH"]
        user = auth.create_user(email=email, password=senha)
        return jsonify({
            "mensagem": "Usuário criado com sucesso!",
            "uid": user.uid,
            "email": user.email
        }), 201
    except:
        raise


def login(login, senha):
    try:
        repository = current_app.config["FIREBASE_DB"]
        fornecedores_ref = repository.collection('fornecedores')
        query = fornecedores_ref.where('cnpj', '==', login).where('senha', '==', senha).limit(1).get()    
        if query:
            doc = query[0]
            fornecedor = FornecedorMapper.from_json(doc.to_dict())
            return fornecedor.id
        else:
            raise ValueError("CNPJ ou senha inválidos.")
    except Exception as e:
        raise ValueError(f"Erro ao tentar fazer login: {str(e)}")
