import requests
from bs4 import BeautifulSoup
import json

# Acessa diretamente a página do CDI no Status Invest
url = "https://statusinvest.com.br/indices/cdi"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # O valor do CDI está dentro de um span com atributo data-testid="index-last"
    span = soup.find("span", {"data-testid": "index-last"})

    if span:
        cdi_text = span.get_text().strip().replace("%", "").replace(",", ".")
        try:
            cdi_value = float(cdi_text)
            with open("cdi.json", "w") as f:
                json.dump({"cdi": cdi_value}, f, indent=2)
            print(f"CDI atualizado com sucesso: {cdi_value}%")
        except ValueError:
            raise Exception("Erro ao converter valor do CDI.")
    else:
        raise Exception("Não foi possível encontrar o valor do CDI na página.")
else:
    raise Exception(f"Erro ao acessar a página. Código {response.status_code}")
