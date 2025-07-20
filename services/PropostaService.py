from flask import current_app
import requests
import json

def gerar_pdf(data):
    api_key = current_app.config.get("ApiDeepSeekKey")

    prompt = f"""
    Quero que você gere um HTML com layout próprio para exportação em PDF. Esse HTML deve representar uma proposta de preços formal, como usada em processos de licitação pública.
    Atenção, vou te mandar os dados que você deve colocar no HTML, em formato JSON, e você deve gerar o HTML com base nesses dados.

    O template base é esse (incluindo o estilo CSS e estrutura do documento), retorne APENAS o HTML com o style no inicio e as tags, sem o <head>,<html>,<body>, sem comentários ou explicações adicionais, apenas o HTML completo:

    { """
        <style>
            div {
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                margin: 40px;
                background-color: #fdfdfd;
                color: #333;
            }

            h1, h2, h3, p {
                margin: 10px 0;
            }

            h1 {
                text-align: center;
                font-size: 22pt;
                color: #2c3e50;
            }

            h2 {
                font-size: 14pt;
                margin-top: 20px;
                color: #2c3e50;
            }

            h3 {
                font-size: 13pt;
                margin-top: 15px;
            }

            .textbox {
                border: 2px solid #000;
                padding: 10px;
                margin-top: 10px;
                background-color: #fff;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 25px;
            }

            table td, table th {
                border: 1px solid #333;
                padding: 8px;
                font-size: 11pt;
            }

            table th {
                background-color: #FBD4B4;
                text-align: center;
            }

            .center {
                text-align: center;
            }

            .right {
                text-align: right;
            }

            .section-title {
                font-weight: bold;
                font-size: 13pt;
                margin-top: 30px;
                color: #1a1a1a;
            }

            .assinatura {
                margin-top: 60px;
                text-align: center;
            }

            .assinatura span {
                display: block;
                margin-top: 5px;
            }

            .small-text {
                font-size: 10pt;
                color: #555;
            }
        </style>

        <h1>PREGÃO ELETRÔNICO Nº: PROCESSO ADMINISTRATIVO:</h1>

        <h3>Órgão:</h3>

        <div class="textbox">
            <strong>Objeto da licitação:</strong>
        </div>

        <div class="textbox">
            <p><strong>RAZÃO SOCIAL:</strong></p>
            <p><strong>CNPJ:</strong></p>
            <p><strong>INSCRIÇÃO ESTADUAL:</strong></p>
            <p><strong>ENDEREÇO:</strong></p>
            <p><strong>CIDADE:</strong></p>
            <p><strong>TELEFONE:</strong></p>
            <p><strong>EMAIL:</strong></p>
            <p><strong>AGÊNCIA:</strong></p>
            <p><strong>CONTA CORRENTE:</strong> BANCO:</p>
        </div>

        <div class="textbox">
            <p><strong>DADOS DO PREPOSTO</strong></p>
            <p>Nome:</p>
            <p>RG:</p>
            <p>CPF:</p>
            <p>Cargo/Função: Estado Civil: Telefone/WhatsApp: E-mail:</p>
        </div>

        <div class="center section-title">PROPOSTA COMERCIAL</div>

        <table>
            <tr>
                <td colspan="6" class="center"><strong>LOTE 01</strong></td>
            </tr>
            <tr>
                <th>ITEM</th>
                <th>DESCRIÇÃO</th>
                <th>UND</th>
                <th>QTD</th>
                <th>V. UNIT.</th>
                <th>V. TOTAL</th>
            </tr>
            <tr>
                <td class="center">1</td>
                <td>Exemplo de Produto</td>
                <td class="center">UN</td>
                <td class="center">10</td>
                <td class="right">R$ 80,70</td>
                <td class="right">R$ 807,00</td>
            </tr>
            <tr>
                <td colspan="5" class="right"><strong>TOTAL</strong></td>
                <td class="right"><strong>R$ 807.079,90</strong></td>
            </tr>
        </table>

        <div class="section-title">CONDIÇÕES COMERCIAIS</div>
        <h2>Prazo de validade da proposta:</h2>
        <h2>Prazo de entrega: <span class="small-text">De acordo com o estabelecido no edital.</span></h2>
        <h2>Local de entrega: <span class="small-text">Conforme orientação do contratante.</span></h2>
        <h2>Condições de pagamento: <span class="small-text">Conforme o estabelecido no edital.</span></h2>

        <div class="section-title">DECLARAÇÕES</div>
        <p>Em cumprimento à Lei Federal nº 14.133/2021, DECLARAMOS:</p>
        <ul>
            <li>Estar em conformidade com todas as exigências legais referentes à habilitação jurídica, regularidade fiscal, trabalhista, qualificação técnica e econômico-financeira;</li>
            <li>Atender integralmente ao objeto da contratação, conforme as especificações exigidas;</li>
            <li>Não possuir impedimentos legais para participar de licitações ou contratar com a Administração Pública;</li>
            <li>Ter ciência e concordância com todas as condições estabelecidas no Edital/Processo de Contratação.</li>
        </ul>

        <p class="right">Ibiassucê, 12 de julho de 2025.</p>

        <div class="assinatura">
            <hr style="width: 300px;">
            <span>Preposto RG:</span>
        </div>

 """}

    O JSON com os dados é esse:
    {json.dumps(data, ensure_ascii=False, indent=2)}
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
    )

    if response.status_code != 200:
        raise Exception(f"Erro ao chamar API: {response.status_code} - {response.text}")

    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
