from blockcypher import simple_spend
from flask import Flask, request, redirect

# external modules
import json
import requests

# internal modules
import api
import krakenComm
import wallet
import math

app = Flask(__name__)

vendor_address = wallet.get_vendor_address()
vendor_private = wallet.get_vendor_private_key()

trader_address = wallet.get_trader_address()

blocktrail_url = "https://api.blocktrail.com/v1/tbtc"
blockcypher_url = "https://api.blockcypher.com/v1/btc/test3"

balance = {"myCHrjWxqSbtHGsaMjtQMXLgyWM22qmQk3": 5000}

@app.route("/get_money")
def get_money():
    address = request.args.get("address")
    money = balance[address]
    return json.dumps({"result": money})

@app.route("/buy_coins")
def buy():
    trader_address = request.args.get("address")
    usd = float(request.args.get("usd"))
    print(str(usd))
    price = float(request.args.get("price"))
    print(str(price))
    if (balance[trader_address] > usd):    
        amount = usd/price*100000000*2
        amount = int(amount)
        print(str(amount))
        response = simple_spend(from_privkey=vendor_private, to_address=trader_address, to_satoshis=math.floor(amount), api_key = api.get_blockcypher_api(), coin_symbol="btc-testnet")
        balance[trader_address] -= usd
        return json.dumps({"status": 200})
    else:
        return json.dumps({"status": 500})

@app.route("/sell_coins")
def sell():
    trader_address = request.args.get("address")
    usd = float(request.args.get("usd"))
    balance[trader_address] += usd
    return json.dumps({"status": 200})


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

@app.route("/sell")
def send():
    from_addr = request.args.get("from")
    to_addr = request.args.get("to")
    value = request.args.get("value")
    print(from_addr)
    print(to_addr)
    print(value)
    response = send_transaction(str(from_addr), str(to_addr), int(value))
    return json.dumps(response)

@app.route("/get_closings_by_fast_forward")
def get_closings_in_range():
    start = request.args.get("start")
    days = request.args.get("days")
    currency = request.args.get("currency")
    krakenConnection = krakenComm.BECon("localhost:5000")
    response = krakenConnection.getClosingValuesInRange(start, days, currency)
    return json.dumps({"result": response})

@app.route("/get_initial_closings")
def get_initial_closings():
    timestamp = request.args.get("timestamp")
    currency = request.args.get("currency")
    krakenConnection = krakenComm.BECon("localhost:5000")
    result = krakenConnection.getClosingValues(timestamp, currency)
    return json.dumps({"result": result})

def get_wallet_balance(wallet_address):
    url = "{0}/addrs/{1}/balance".format(blockcypher_url, wallet_address)
    response = requests.get(url)
    return response.json()

def get_wallet_transactions(wallet_address):
    url = "{0}/address/{1}/transactions".format(blocktrail_url, wallet_address)
    payload = {"api_key" : blocktrail_public}
    response = requests.get(url, params=payload)
    return response.json()


