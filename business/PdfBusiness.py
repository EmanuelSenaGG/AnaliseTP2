import pdfplumber
import re

def extrair_texto_pdf(caminho_arquivo):
    texto = ""
    with pdfplumber.open(caminho_arquivo) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    texto = limpar_texto(texto)
    return texto



def limpar_texto(texto):
    texto = re.sub(r'[ \t]+', ' ', texto)  # normaliza espaços
    texto = re.sub(r'\n\s*\n+', '\n\n', texto)  # preserva parágrafos
    return texto.strip()
