class Licitacao:
    def __init__(
        self,
        id,
        objeto,
        empresa,
        cnpj,
        responsavel,
        email,
        telefone,
        pregao_eletronico,
        processo,
        nome_arquivo,
        caminho_arquivo,
        fornecedores_vinculados=None,
      
    ):
        self.id = id
        self.objeto = objeto
        self.empresa = empresa
        self.cnpj = cnpj
        self.responsavel = responsavel
        self.email = email
        self.telefone = telefone
        self.nome_arquivo = nome_arquivo
        self.caminho_arquivo = caminho_arquivo
        self.fornecedores_vinculados = fornecedores_vinculados or []
        self.pregao_eletronico = pregao_eletronico
        self.processo = processo

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data.get("id"),
            objeto=data.get("objeto"),
            empresa=data.get("empresa"),
            cnpj=data.get("cnpj"),
            responsavel=data.get("responsavel"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            nome_arquivo=data.get("nome_arquivo"),
            caminho_arquivo=data.get("caminho_arquivo"),
            fornecedores_vinculados=data.get("fornecedores_vinculados", []),
            pregao_eletronico=data.get("pregao_eletronico"),
            processo=data.get("processo")
        )

    def to_json(self):
        return {
            "id": self.id,
            "objeto": self.objeto,
            "empresa": self.empresa,
            "cnpj": self.cnpj,
            "responsavel": self.responsavel,
            "email": self.email,
            "telefone": self.telefone,
            "nome_arquivo": self.nome_arquivo,
            "caminho_arquivo": self.caminho_arquivo,
            "fornecedores_vinculados": self.fornecedores_vinculados,
            "pregao_eletronico": self.pregao_eletronico,
            "processo": self.processo
        }
