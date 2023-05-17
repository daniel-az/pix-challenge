import requests
import json
import os

server_url = os.environ.get('server_url', 'http://localhost:8000/')

def search_key(key):
    url = "{}search?key={}".format(server_url,key)
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        raise Exception("Erro na requisição")

def transfer(sender, recipient, value):
    data = {
        "sender": sender,
        "recipient": recipient,
        "value": value
    }
    headers = {'Content-Type': 'application/json'}
    url = "{}transfer".format(server_url)
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erro na transferência")

# Exemplo de uso
key = "772384558"
result = search_key(key)

if result is not None:
    sender = "772384558"
    recipient = key
    value = 10.0
    transfer_result = transfer(sender, recipient, value)
    print("Transferência realizada:")
    print(transfer_result)
else:
    print("Chave não encontrada")
