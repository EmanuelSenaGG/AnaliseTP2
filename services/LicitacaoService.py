from uuid import uuid4
from flask import current_app
from models.Licitacao import Licitacao as LicitacaoMapper

def cadastrar_licitacao(data):
    try:
        licitacao = LicitacaoMapper.from_json(data)
        repository = current_app.config["FIREBASE_DB"]
        id = str(uuid4())
        licitacao.id = id
        repository.collection("licitacoes").document(id).set(licitacao.to_json())
        return 
    except :
        raise


def listar_licitacoes():
    try:
        repository = current_app.config["FIREBASE_DB"]
        docs = repository.collection("licitacoes").stream()
        licitacoes = []
        for doc in docs:
            licitacao = LicitacaoMapper.from_json(doc.to_dict())
            licitacoes.append(licitacao)
        return licitacoes
    except:
        raise
    
def registrar_vinculos(licitacao_id, fornecedores):
    try:
        repository = current_app.config["FIREBASE_DB"]
        doc_ref = repository.collection("licitacoes").document(licitacao_id)
        licitacao = doc_ref.get().to_dict()
        
        if not licitacao:
            raise ValueError("Licitação não encontrada")

        vinculos = licitacao.get("fornecedores_vinculados", [])
        vinculos_set = set(vinculos)
        vinculos_set.update(fornecedores)
        vinculos = list(vinculos_set)
        doc_ref.update({"fornecedores_vinculados": vinculos})
        return 
    except:
        raise 

def listar_licitacoes_fornecedor(id_fornecedor):
    try:
        repository = current_app.config["FIREBASE_DB"]
        docs = repository.collection("licitacoes").where("fornecedores_vinculados", "array_contains", id_fornecedor).stream()
        licitacoes = []
        for doc in docs:
            licitacao = LicitacaoMapper.from_json(doc.to_dict())
            licitacoes.append(licitacao)
        return licitacoes
    except:
        raise
    
def obter_licitacao_por_id(id_licitacao):
    try:
        repository = current_app.config["FIREBASE_DB"]
        doc = repository.collection("licitacoes").document(id_licitacao).get()  
        if doc.exists:
            data = doc.to_dict()
            return LicitacaoMapper.from_json(data)
        else:
            raise ValueError(f"Licitacao com ID '{id_licitacao}' não encontrada.")   
    except:
        raise 
    
def obter_path_arquivo_licitacao_por_id(id_licitacao):
    try:
        repository = current_app.config["FIREBASE_DB"]
        doc = repository.collection("licitacoes").document(id_licitacao).get()  
        if doc.exists:
            data = doc.to_dict()
            return LicitacaoMapper.from_json(data).caminho_arquivo
        else:
            raise ValueError(f"Licitacao com ID '{id_licitacao}' não encontrada.")   
    except:
        raise 

