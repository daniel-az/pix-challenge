# **PIX  Challenge** #
Repositório com o server do desafio do pix do Nubank

# **Pré-requisitos** #
- Python 3
- Pip

# **Instalação de Dependências** #
```shell
pip install -r requirements.txt
```

# **Execução do Servidor** #
```shell
python server.py
```

# **End-points** #

## **Busca de Chave** ##
End-point do tipo GET responsável por recuperar uma chave PIX de um determinado usuário na base de dados do Banco Central.
```
/search?key=772384558
```

### Parâmetros ###
- **key** - parâmetro da chave pix reponsável por encontrar o usuário na base de dados do Banco Central

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

## **Transação de Valores** ##
End-point do tipo POST responsável por realizar uma transação entre duas contas que possuem chaves pix.

### Exemplo de chamada ###
```shell
curl -d '{"sender": "772384558", "recipient":"176086599", "value": 1.0}' -H "Content-Type: application/json" -X POST http://localhost:5000/transfer
```

### Request Body ###
```json
{
    "sender": "772384558", 
    "recipient": "176086599", 
    "value": 1.0
}
```
- **sender** - chave pix do usuário que está enviando o valor
- **recipient** - chave pix do usuário que irá receber o valor
- **value** - valor da transferência

### Response ###
```json
{
    "recipient": "176086599",
    "sender": "772384558",
    "transaction_id": "7b6bcda5c19cb4075e0dc995146f8c5f",
    "value": 1.0
}
```