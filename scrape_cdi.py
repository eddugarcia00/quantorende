import requests
import json

url = "https://statusinvest.com.br/indicadores/taxasdi"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    cdi = data.get("value")

    if cdi:
        with open("cdi.json", "w") as f:
            json.dump({"cdi": cdi}, f, indent=2)
        print(f"CDI atualizado com sucesso: {cdi}")
    else:
        raise Exception("Valor do CDI não encontrado na resposta.")
else:
    raise Exception(f"Erro ao acessar a API. Código {response.status_code}")
