# **PIX  Challenge** #
Repositório com o client/consumer do desafio do pix do Nubank

# **Pré-requisitos** #
- Python 3
- Pip
- docker
- rabbitmq

# **Instalação de Dependências** #
```shell
pip install -r requirements.txt
```
# **Execução do RabbitMQ** #
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management

# **Criação de filas para o RabbitMQ via Comando ** #
rabbitmqadmin declare queue name=transfer_queue durable=false

# **Criação de filas para o RabbitMQ via Interface Gráfica ** #

1. Acesse o RabbitMQ Management UI no seu navegador, normalmente em http://localhost:15672.
2. Faça login com suas credenciais de administrador.
3. Navegue até a seção "Queues" no painel de controle.
4. Clique no botão "Add a new queue" (ou similar) para criar uma nova fila.
5. Preencha o nome da fila como transfer_queue e configure outras opções, se necessário.
6. Clique em "Add queue" ou "Create" para criar a fila.

# **Execução do Consumer** #
```shell
python consumer.py
```

# **Execução do Client** #
```shell
python client.py
```

# **Queues** #

## ** Dados para transferência de valores via fila** ##
Fila de RabbitMQ chamada transfer_queue. 

### Exemplo de post na fila ###

```
{
    "sender": "772384558",
    "recipient": "772384558",
    "value": 10
}
```
- **sender** - chave pix do usuário que está enviando o valor
- **recipient** - chave pix do usuário que irá receber o valor
- **value** - valor da transferência

### Parâmetros ###
Exemplos de chaves válidas para serem enviadas como **recipient**

|chave|usuário|banco|
|-|-|-|    
|772384558|Ausnia|Nubank|
|176086599|Dundîr|Bradesco|
|423405201|Orokgu|Banrisul|
|972593349|Buruol|Bradesco|
|224779509|Xuhogi|Santander|
|899383393|Seakar|Caixa Econômica Federal|
|308903263|Khadzu|Itau|
|630706443|Elzile|Safra|
|150822608|Bedudo|Banco de Brasil|

### Response no log da aplicacao ###
```json
{
    "recipient": "176086599",
    "sender": "772384558",
    "transaction_id": "7b6bcda5c19cb4075e0dc995146f8c5f",
    "value": 1.0
}
```