# AnáliseTP2

Este projeto é um sistema web que utiliza a API do Gemini para diversas funcionalidades. Siga as instruções abaixo para configurar e executar o projeto em sua máquina.

-----

## Pré-requisitos

Certifique-se de que o **Python** esteja instalado em sua máquina. Versão 3.12.0

-----

## Configuração e Instalação

Siga os passos abaixo para configurar o ambiente virtual e instalar as dependências.

### 1\. Criar e Ativar o Ambiente Virtual

No diretório raiz do projeto (`AnaliseTP2`), crie um ambiente virtual chamado `.venv` com o seguinte comando:

```bash
python -m venv .venv
```

Em seguida, ative o ambiente virtual. O comando pode variar dependendo do seu sistema operacional:

```bash
# Para Windows PowerShell
.venv/Scripts/activate.ps1

# Para outras plataformas (macOS/Linux)
source .venv/bin/activate
```

Você saberá que o ambiente está ativado quando `(.venv)` aparecer no início da linha de comando.

### 2\. Instalar as Dependências

Com o ambiente virtual ativado, instale todas as dependências do projeto listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

-----

## Configurando a Chave de API do Gemini

Para utilizar o projeto, você precisa de uma chave de API válida para o Gemini.

1.  **Obtenha sua chave:** Acesse o [Google IA Studio](https://aistudio.google.com/) e obtenha uma chave de API gratuita.
2.  **Adicione a chave ao projeto:** Abra o arquivo `app.py` e localize a linha `app.config["ApiGeminiKey"] = "SUA KEY AQUI"`. Substitua `"SUA KEY AQUI"` pela sua chave de API.

<!-- end list -->

```python
# Exemplo de como deve ficar após a substituição
app.config["ApiGeminiKey"] = "SUA-CHAVE-DE-API-VALIDA"
```

-----

## Como Executar o Projeto

1.  Após instalar as dependências e configurar a chave de API, abra o arquivo `app.py` em seu ambiente de desenvolvimento e execute-o.
2.  Execute o arquivo `app.py` no terminal, com o ambiente virtual ativado:

<!-- end list -->

```bash
python app.py
```

3.  Após executar, você verá uma saída semelhante a esta no terminal:

<!-- end list -->

```bash
* Serving Flask app 'app'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

4.  Acesse a URL `http://127.0.0.1:5000` em seu navegador para começar a usar o sistema\!
5.  Utilize as credenciais "admin" em ambos os campos para entrar como administrador\!
