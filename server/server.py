from flask import Flask, request
import json
import hashlib
import datetime
from jsonschema import validate


app = Flask(__name__)

key_database = {
                "772384558": {"name": "Ausnia",     "bank": "Nubank"},
                "176086599" :{"name": "Dundîr",     "bank": "Bradesco"},
                "423405201" :{"name": "Orokgurz",   "bank": "Banrisul"},
                "972593349" :{"name": "Buruolg",    "bank": "Bradesco"},
                "224779509" :{"name": "Xuhogil",    "bank": "Santander"},
                "899383393" :{"name": "Seakare",    "bank": "Caixa Econômica Federal"},
                "308903263" :{"name": "Khadzuma",   "bank": "Itau"},
                "630706443" :{"name": "Elziley",    "bank": "Safra"},
                "150822608" :{"name": "Bedudor",    "bank": "Banco de Brasil"},
                }

class SearchKey(object):
    def __init__(self, key):
        self.key = key

    def get(self):
        return json.dumps(key_database[self.key])


class Transaction(object):
    def is_valid_json(self, transaction):
        schema = {
            "type" : "object",
            "properties" : {
                "sender" : {"type" : "string"},
                "recipient" : {"type" : "string"},
                "value" : {"type" : "number"},
            },
        }
        payload = json.loads(transaction)
        validate(instance=payload, schema=schema)
        return payload

    def __init__(self, transaction):
        self.transaction = self.is_valid_json(transaction)

        self.sender = self.transaction["sender"]
        self.recipient = self.transaction["recipient"]
        self.value = self.transaction["value"]

    def __str__(self):
        return json.dumps(self.transaction)


class TransferValue(object):
    def __init__(self, transfer_object):
        self.transaction = transfer_object

    def execute(self):
        id_transaction = hashlib.md5(
            "{transaction}-{time_transaction}".format(
                transaction=str(self.transaction),
                time_transaction=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")).encode('utf-8')
        ).hexdigest()

        return {
            "sender" : self.transaction.sender,
            "recipient": self.transaction.recipient,
            "value": self.transaction.value,
            "transaction_id": id_transaction
            }

"""
    /search?key=772384558
"""
@app.route("/search", methods=["GET"])
def search() -> str:
    key = request.args.get('key')
    service = SearchKey(key)
    try:
       return service.get()
    except KeyError:
        return "Key not found", 404

"""
    {
        "sender":"pix key",
        "recipient":"pix key",
        "value":1.00
    }
"""
@app.route("/transfer", methods=["POST"])
def transfer() -> str:
    trasaction = Transaction(request.data)
    service = TransferValue(trasaction)
    return service.execute()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
