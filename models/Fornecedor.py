class Fornecedor:
    def __init__(
        self,
        id,
        razao_social,
        senha,
        cnpj,
        inscricao_estadual,
        endereco,
        cidade,
        telefone,
        email,
        caminho_logomarca,
        nome_logomarca,
        agencia,
        conta_corrente,
        banco,
        preposto_nome,
        preposto_rg,
        preposto_cpf,
        preposto_cargo,
        preposto_estado_civil,
        preposto_telefone,
        preposto_email
    ):
        self.id = id
        self.razao_social = razao_social
        self.senha = senha
        self.cnpj = cnpj
        self.inscricao_estadual = inscricao_estadual
        self.endereco = endereco
        self.cidade = cidade
        self.telefone = telefone
        self.email = email
        self.agencia = agencia
        self.conta_corrente = conta_corrente
        self.banco = banco
        self.preposto_nome = preposto_nome
        self.preposto_rg = preposto_rg
        self.preposto_cpf = preposto_cpf
        self.preposto_cargo = preposto_cargo
        self.preposto_estado_civil = preposto_estado_civil
        self.preposto_telefone = preposto_telefone
        self.preposto_email = preposto_email
        self.caminho_logomarca = caminho_logomarca
        self.nome_logomarca = nome_logomarca

    @classmethod
    def from_json(cls, data):
        return cls(
            id = data.get("id"),
            razao_social=data.get("razao_social"),
            senha=data.get("senha"),
            cnpj=data.get("cnpj"),
            inscricao_estadual=data.get("inscricao_estadual"),
            endereco=data.get("endereco"),
            cidade=data.get("cidade"),
            telefone=data.get("telefone"),
            email=data.get("email"),
            agencia=data.get("agencia"),
            conta_corrente=data.get("conta_corrente"),
            banco=data.get("banco"),
            preposto_nome=data.get("preposto_nome"),
            preposto_rg=data.get("preposto_rg"),
            preposto_cpf=data.get("preposto_cpf"),
            preposto_cargo=data.get("preposto_cargo"),
            preposto_estado_civil=data.get("preposto_estado_civil"),
            preposto_telefone=data.get("preposto_telefone"),
            preposto_email=data.get("preposto_email"),
            caminho_logomarca=data.get("caminho_logomarca"),
            nome_logomarca=data.get("nome_logomarca")
        )

    def to_json(self):
        return {
            "id": self.id,
            "razao_social": self.razao_social,
            "senha": self.senha,
            "cnpj": self.cnpj,
            "inscricao_estadual": self.inscricao_estadual,
            "endereco": self.endereco,
            "cidade": self.cidade,
            "telefone": self.telefone,
            "email": self.email,
            "agencia": self.agencia,
            "conta_corrente": self.conta_corrente,
            "banco": self.banco,
            "preposto_nome": self.preposto_nome,
            "preposto_rg": self.preposto_rg,
            "preposto_cpf": self.preposto_cpf,
            "preposto_cargo": self.preposto_cargo,
            "preposto_estado_civil": self.preposto_estado_civil,
            "preposto_telefone": self.preposto_telefone,
            "preposto_email": self.preposto_email,
            "caminho_logomarca": self.caminho_logomarca,
            "nome_logomarca": self.nome_logomarca
        }

