from turtle import delay
import requests
import json
import os
import pika
from jsonschema import validate
from retry import retry

server_url = os.environ.get('server_url', 'http://localhost:8000/')
queue_address = os.environ.get('queue_address', '127.0.0.1')

def is_valid_json(transaction):
    schema = {
        "type" : "object",
        "required": [ "sender", "recipient", "value" ],
        "properties" : {
            "sender" : {"type" : "string"},
            "recipient" : {"type" : "string"},
            "value" : {"type" : "number"},
        },
    }
    payload = json.loads(transaction)
    try:
        validate(instance=payload, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Json inválido"
        return False, err
    return True

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

def callback(ch, method, properties, body):
    if is_valid_json(body.decode('utf-8')) is True:
        data = json.loads(body.decode('utf-8'))
        sender = data['sender']
        recipient = data['recipient']
        value = data['value']

        result = search_key(recipient)
        if result is not None:
            transfer_result = transfer(sender, recipient, value)
            print("Transferência realizada:")
            print(transfer_result)
        else:
            print("Chave não encontrada")
    else:
        print("Json inválido")

# Configurações de conexão com o RabbitMQ
@retry(tries=3, delay=10)
def connect_rabbitmq():
    return pika.BlockingConnection(pika.ConnectionParameters(queue_address))
try:
    connection = connect_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='transfer_queue')

    # Configuração do consumidor
    channel.basic_consume(queue='transfer_queue', on_message_callback=callback, auto_ack=True)

    # Início do consumo de mensagens
    print('Aguardando mensagens. Pressione CTRL+C para sair.')
    channel.start_consuming()
except Exception as e:
    print(f"Erro na conexão com o RabbitMQ: {str(e)}")
    print(queue_address)
finally:
    if connection:
        connection.close()