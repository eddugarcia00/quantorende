import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://statusinvest.com.br/indices/cdi"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

value_element = soup.select_one("h3 span.value")
if value_element:
    cdi_text = value_element.text.strip().replace("%", "").replace(",", ".")
    cdi_value = float(cdi_text)

    cdi_data = {
        "data": datetime.now().strftime("%Y-%m-%d"),
        "valor": cdi_value
    }

    with open("public/cdi.json", "w") as f:
        json.dump(cdi_data, f, indent=2)
else:
    raise Exception("Não foi possível encontrar o valor do CDI.")
