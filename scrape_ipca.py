import requests
from bs4 import BeautifulSoup
import json

# URL da página do IBGE com os valores de inflação
url = "https://www.ibge.gov.br/explica/inflacao.php"

# Faz a requisição
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    raise Exception(f"Erro ao acessar a página. Código {response.status_code}")

# Faz o parsing do HTML
soup = BeautifulSoup(response.text, "html.parser")

# Procura todos os elementos com class "variavel"
variaveis = soup.select("li.variavel")

ipca_12m = None

# Busca aquele que tem o título correto
for var in variaveis:
    titulo = var.find("h3", class_="variavel-titulo")
    if titulo and "IPCA acumulado de 12 meses" in titulo.text:
        dado = var.find("p", class_="variavel-dado")
        if dado:
            ipca_12m = dado.text.strip()
            break

if not ipca_12m:
    raise Exception("Não foi possível extrair o valor acumulado de 12 meses do IPCA.")

# Salva em um arquivo JSON
with open("ipca12m.json", "w") as f:
    json.dump({"ipca12m": ipca_12m}, f, indent=2)

print(f"IPCA acumulado de 12 meses: {ipca_12m}")
