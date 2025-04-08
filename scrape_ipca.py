import requests
from bs4 import BeautifulSoup
import json

# URL da página do IBGE com os dados de inflação
url = "https://www.ibge.gov.br/explica/inflacao.php"

# Fazendo a requisição com headers simulando um navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

# Verifica se a requisição foi bem-sucedida
if response.status_code != 200:
    raise Exception(f"Erro ao acessar a página. Código {response.status_code}")

# Faz o parse do HTML
soup = BeautifulSoup(response.content, "html.parser")

# Busca todos os blocos <li class="variavel">
variaveis = soup.find_all("li", class_="variavel")

ipca_12m = None
for var in variaveis:
    titulo = var.find("h3", class_="variavel-titulo")
    if titulo and "acumulado de 12 meses" in titulo.text:
        dado = var.find("p", class_="variavel-dado")
        if dado:
            ipca_12m = dado.text.strip()
            break

if not ipca_12m:
    raise Exception("Não foi possível extrair o valor acumulado de 12 meses do IPCA.")

# Salva em arquivo JSON
data = {"ipca_12m": ipca_12m}
with open("ipca12m.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"IPCA acumulado em 12 meses: {ipca_12m}")
