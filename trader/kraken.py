from flask import Flask, request

# external modules
import json
import requests

# internal modules
import api
import wallet

app = Flask(__name__)

blocktrail_public = api.get_blocktrail_public()
blocktrail_secret = api.get_blocktrail_secret()

trader_address = wallet.get_trader_address()
trader_passcode = wallet.get_trader_passcode()

vendor_address = wallet.get_vendor_address()
vendor_passcode = wallet.get_vendor_passcode()

blocktrail_url = "https://api.blocktrail.com/v1/tbtc"
blockcypher_url = "https://api.blockcypher.com/v1/btc/test3"

client = None
trader = None

@app.route("/")
def hello():
    strings = []
    response = send_transaction(vendor_address, trader_address, 100)
    print(str(response))

    strings.append(get_wallet_balance(trader_address))
    strings.append(get_wallet_balance(vendor_address))
    return json.dumps({"result": strings}) 

@app.route("/balance")
def get_balance():
    address = request.args.get("address")
    return json.dumps(get_wallet_balance(address))
   
@app.route("/send_transaction")
def send():
    from_addr = request.args.get("from")
    to_addr = request.args.get("to")
    value = request.args.get("value")
    print(from_addr)
    print(to_addr)
    print(value)
    response = send_transaction(str(from_addr), str(to_addr), int(value))
    return json.dumps(response)

def get_wallet_balance(wallet_address):
    url = "{0}/addrs/{1}/balance".format(blockcypher_url, wallet_address)
    payload = {"api_key": blocktrail_public}
    response = requests.get(url, params=payload)
    return response.json()

def get_wallet_transactions(wallet_address):
    url = "{0}/address/{1}/transactions".format(blocktrail_url, wallet_address)
    payload = {"api_key" : blocktrail_public}
    response = requests.get(url, params=payload)
    return response.json()

def send_transaction(from_wallet, to_wallet, amount):
    body = {
        "inputs": [
            {
                "addresses": [from_wallet],
            }    
        ],
        "outputs": [
            {
                "addresses": [to_wallet],
                "value": amount
            }    
        ]
    }
    url = "{0}/txs/new".format(blockcypher_url)
    response = requests.post(url, data = json.dumps(body))
    return response.json()


