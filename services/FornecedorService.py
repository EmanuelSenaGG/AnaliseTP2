from uuid import uuid4
from flask import current_app
from models.Fornecedor import Fornecedor as FornecedorMapper

def cadastrar_fornecedor(data):
    try:
        fornecedor = FornecedorMapper.from_json(data)
        repository = current_app.config["FIREBASE_DB"]
        fornecedor_id = str(uuid4())
        fornecedor.id = fornecedor_id
        repository.collection("fornecedores").document(fornecedor_id).set(fornecedor.to_json())
        return
    except :
        raise


def listar_fornecedores():
    try:
        repository = current_app.config["FIREBASE_DB"]
        docs = repository.collection("fornecedores").stream()
        fornecedores = []
        for doc in docs:
            fornecedor = FornecedorMapper.from_json(doc.to_dict())
            fornecedores.append(fornecedor)
        return fornecedores 
    except:
        raise
    
def obter_fornecedor_por_id(id_fornecedor):
    try:
        repository = current_app.config["FIREBASE_DB"]
        doc = repository.collection("fornecedores").document(id_fornecedor).get()
        if doc.exists:
            return FornecedorMapper.from_json(doc.to_dict())
        else:
            raise ValueError("Fornecedor não encontrado")
    except:
        raise 