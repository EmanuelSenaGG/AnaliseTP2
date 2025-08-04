import re
import json
from business import PdfBusiness
from flask import current_app, url_for
from google import genai
from datetime import datetime, timedelta
import os
from flask import  request
from jinja2 import Template
from services import LicitacaoService as _licitacaoService
from services import FornecedorService as _serviceFornecedor


def analisar_pdf(arquivoPath):
    text_context = PdfBusiness.extrair_texto_pdf(arquivoPath)
    api_key = current_app.config.get("ApiGeminiKey")
    client = genai.Client(api_key=api_key)

    try:   
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
                        Analise o texto abaixo e extraia todos os itens listados nele. Não oculte nenhum item, mesmo que não tenha preço ou quantidade ou que tenha descrição parecida.

                        Para cada item identificado, retorne um **único JSON** contendo uma lista de objetos, onde cada objeto representa um item com os seguintes campos:

                        - **descricao**: descrição do item  
                        - **unidade**: unidade de medida (ex: kg, m, un, etc.)  
                        - **quantidade**: quantidade do item  
                        - **preco**: preço unitário  
                        - **valor_total**: valor total do item (quantidade × preço)

                        Não inclua nenhuma explicação ou texto adicional. A resposta deve conter **apenas o JSON** válido.

                        Texto para análise:
                        {text_context}
                        """
        )

        json_result = json.loads(response.text)
    except:
        json_result = extrair_json_lista(response.text)

    return json_result


def analisar_pdf2(arquivoPath):
    itens = [
        {"descricao": "Caderno universitário capa dura 200 folhas", "unidade": "UN", "quantidade": 10, "preco": 18.50, "valor_total": 185.00},
        {"descricao": "Caneta esferográfica azul", "unidade": "UN", "quantidade": 100, "preco": 1.20, "valor_total": 120.00},
        {"descricao": "Papel sulfite A4 75g/m² pacote com 500 folhas", "unidade": "PC", "quantidade": 25, "preco": 22.90, "valor_total": 572.50},
        {"descricao": "Toner compatível para impressora HP 12A", "unidade": "UN", "quantidade": 4, "preco": 68.75, "valor_total": 275.00},
        {"descricao": "Grampeador metálico grande", "unidade": "UN", "quantidade": 8, "preco": 34.90, "valor_total": 279.20},
        {"descricao": "Caixa organizadora plástica 40L", "unidade": "UN", "quantidade": 5, "preco": 45.00, "valor_total": 225.00},
        {"descricao": "Mouse óptico USB", "unidade": "UN", "quantidade": 12, "preco": 29.90, "valor_total": 358.80},
        {"descricao": "Teclado USB padrão ABNT2", "unidade": "UN", "quantidade": 10, "preco": 55.00, "valor_total": 550.00},
        {"descricao": "Cabo HDMI 1.5m", "unidade": "UN", "quantidade": 15, "preco": 19.90, "valor_total": 298.50},
        {"descricao": "Lixeira plástica com pedal 50L", "unidade": "UN", "quantidade": 6, "preco": 85.00, "valor_total": 510.00},
        {"descricao": "Álcool em gel 70% 500ml", "unidade": "FR", "quantidade": 30, "preco": 6.50, "valor_total": 195.00},
        {"descricao": "Detergente neutro 500ml", "unidade": "FR", "quantidade": 40, "preco": 3.20, "valor_total": 128.00},
        {"descricao": "Esponja dupla face", "unidade": "UN", "quantidade": 50, "preco": 1.10, "valor_total": 55.00},
        {"descricao": "Fita adesiva larga transparente", "unidade": "RL", "quantidade": 20, "preco": 7.90, "valor_total": 158.00},
        {"descricao": "Bloco de anotações adesivas 76x76mm", "unidade": "UN", "quantidade": 30, "preco": 4.50, "valor_total": 135.00},
        {"descricao": "Marcador de texto amarelo", "unidade": "UN", "quantidade": 25, "preco": 3.75, "valor_total": 93.75},
        {"descricao": "Pasta L plástica", "unidade": "UN", "quantidade": 100, "preco": 0.85, "valor_total": 85.00},
        {"descricao": "Envelope pardo A4", "unidade": "UN", "quantidade": 200, "preco": 0.65, "valor_total": 130.00},
        {"descricao": "Extensão elétrica 3 metros com 3 entradas", "unidade": "UN", "quantidade": 10, "preco": 39.90, "valor_total": 399.00},
        {"descricao": "Cadeira giratória com rodízios", "unidade": "UN", "quantidade": 3, "preco": 420.00, "valor_total": 1260.00},
        {"descricao": "Mesa de escritório retangular 1,20m", "unidade": "UN", "quantidade": 2, "preco": 520.00, "valor_total": 1040.00},
        {"descricao": "Estabilizador 500VA bivolt", "unidade": "UN", "quantidade": 5, "preco": 145.00, "valor_total": 725.00},
        {"descricao": "Filtro de linha com 5 tomadas", "unidade": "UN", "quantidade": 10, "preco": 25.00, "valor_total": 250.00},
        {"descricao": "Copo descartável 200ml", "unidade": "CX", "quantidade": 10, "preco": 12.50, "valor_total": 125.00},
        {"descricao": "Lâmpada LED 9W bivolt", "unidade": "UN", "quantidade": 20, "preco": 9.90, "valor_total": 198.00}
    ]
    
    return itens



def gerar_html_proposta(dados):
    try:
        dados = request.get_json()
        itens = dados.get("itens", [])
        idLicitacao = dados.get("idLicitacao", 0)
        idFornecedor = dados.get("idFornecedor", 0)
        valor_total_gerado = dados.get("valor_total_geral", 0)
        licitacao = _licitacaoService.obter_licitacao_por_id(idLicitacao)
        fornecedor = _serviceFornecedor.obter_fornecedor_por_id(idFornecedor)
        url_logomarca = url_for('static', filename=fornecedor.caminho_logomarca)
        hoje = datetime.now()
        data_emissao = hoje.strftime("%d de %B de %Y") 
        prazo_validade = (hoje + timedelta(days=7)).strftime("%d de %B de %Y")
        template_path = os.path.join(current_app.root_path, "static", "proposta", "proposta_template.html")
        output_path = os.path.join(current_app.root_path, "static", "outputs",f"{fornecedor.razao_social}", f"{fornecedor.razao_social}-proposta-preenchida.html")
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        with open(template_path, encoding="utf-8") as f:
            template = Template(f.read())

        html_resultado = template.render(
            empresa=licitacao,
            fornecedor=fornecedor,
            itens=itens,
            valor_total_geral=valor_total_gerado,
            data_emissao=data_emissao,
            prazo_validade=prazo_validade,
            url_logomarca=url_logomarca
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_resultado)

        url_proposta = url_for('static', filename=f"outputs/{fornecedor.razao_social}/{fornecedor.razao_social}-proposta-preenchida.html")
        return {"url": url_proposta}

    except Exception as e:
        return {"erro": str(e)}, 500
    
    
def extrair_json_lista(string):
    # Expressão regular para localizar JSON do tipo lista de objetos
    padrao = r'\[\s*\{.*?\}\s*\]'  # Captura algo como: [{...}, {...}]
    
    # Flags re.DOTALL para pegar multiline e re.MULTILINE se necessário
    correspondencias = re.findall(padrao, string, re.DOTALL)

    for match in correspondencias:
        try:
            # Tenta fazer o parse do JSON
            json_extraido = json.loads(match)
            # Verifica se é uma lista de dicionários
            if isinstance(json_extraido, list) and all(isinstance(obj, dict) for obj in json_extraido):
                return json_extraido
        except json.JSONDecodeError:
            continue
    
    return None