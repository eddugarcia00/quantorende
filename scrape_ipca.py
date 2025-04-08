import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.ibge.gov.br/explica/inflacao.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(URL, headers=headers)

if response.status_code != 200:
    raise Exception(f"Erro ao acessar a página. Código {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# Procura pelo título IPCA
ipca_title = soup.find("h2", string=lambda text: text and "IPCA" in text)

if not ipca_title:
    raise Exception("Não foi possível encontrar a seção do IPCA na página.")

# Acha o primeiro <p> após o título que contém o valor de 12 meses
ipca_section = ipca_title.find_next("p")

ipca_text = ipca_section.get_text(strip=True)

# Procura o número referente ao acumulado em 12 meses (ex: 4,62%)
import re
match = re.search(r'acumulado.*?12.*?meses.*?([\d,]+)%', ipca_text, re.IGNORECASE)

if not match:
    raise Exception("Não foi possível extrair o valor acumulado de 12 meses do IPCA.")

ipca_12m = match.group(1).replace(",", ".")

# Salva o valor em um arquivo JSON
with open("ipca12m.json", "w") as f:
    json.dump({"ipca_12_meses": float(ipca_12m)}, f, indent=2)

print("IPCA acumulado em 12 meses salvo com sucesso:", ipca_12m)
