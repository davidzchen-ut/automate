from blockcypher import simple_spend
from flask import Flask
from flask import request
from flask import Response
from flask import json
from flask import redirect
from flask import render_template
from flask import url_for
from flask_cors import CORS

# external modules
import datetime
import json
import math
import requests
import time

# internal modules
import algorithm
import api
import wallet

app = Flask(__name__)
CORS(app)

blocktrail_public = api.get_blocktrail_public()
blocktrail_secret = api.get_blocktrail_secret()

trader_private = wallet.get_trader_private_key()
trader_address = wallet.get_trader_address()

vendor_address = wallet.get_vendor_address()

backend_url = "https://99a5dae8.ngrok.io"

client = None
trader = None

date = None
coinPercentages = {}
coinLimits = {}

traderAddress = "2MzLGbQpMF9NEni8AqDRG4HPuUE2QHgG9nN"

current_price = None

transactions = []

@app.route("/")
def good_morning():
    print(app.root_path)
    return render_template("autom8bitcoin.html", transactions=transactions)

def buy_percent():
    url = "{0}/get_money".format(backend_url) 
    payload = {
        "address": trader_address
    }
    response = requests.get(url, params=payload)
    usd_balance = response.json()["result"]
    amount = usd_balance * int(coinPercentages["Bitcoin"]) / 100 * int(coinLimits["Bitcoin"]) / 100
    buy(amount)

def sell_percent():
    url = "{0}/balance".format(backend_url)
    payload = {
        "address": trader_address
    }
    response = requests.get(url, params=payload)
    balance = response.json()["balance"]
    amount = balance * int(coinPercentages["Bitcoin"]) / 100 * int(coinLimits["Bitcoin"]) / 100
    sell(amount)

def buy(usd):
    url = "{0}/buy_coins".format(backend_url)
    payload = {
        "address": trader_address,
        "usd": usd,
        "price": current_price
    }
    if (usd > 0):
        response = requests.get(url, params=payload)
        return ({"status": 200})
    else:
        print("not enough money to buy")
        return json.dumps({"status": 200})

def sell(amount):
    usd = amount * current_price / 100000000
    print(str(usd))

    if (amount > 0):
        response = simple_spend(from_privkey=trader_private, to_address=vendor_address, to_satoshis=math.floor(amount), coin_symbol="btc-testnet", api_key=api.get_blockcypher_api())

        url = "{0}/sell_coins".format(backend_url)
        payload = {
            "address": trader_address,
            "usd": usd
        }
        response = requests.get(url, params=payload)
        return json.dumps({"status": 200})
    else:
        print("not enough bitcoins to sell")
        return json.dumps({"status": 200})

@app.route("/build")
def build():
    global date
    temp_date = request.args.get('date')
    date = time.mktime(datetime.datetime.strptime(temp_date, "%Y-%m-%d").timetuple())
    url = backend_url + "/get_initial_closings"
    payload = {"timestamp": int(date), "currency": "XXBTZUSD"}
    response = requests.get(url, params = payload)
    result = algorithm.initialize(response.json()["result"]) 
    return json.dumps({"status": 200})

@app.route("/fast-forward")
def fastForward():
    global date, current_price
    integer = request.args.get('integer')
    duration = request.args.get('duration')
    if ("day" in duration):
        url = backend_url + '/get_closings_by_fast_forward'
        payload = {"start": int(date), "currency": "XXBTZUSD", "days": int(integer)}
        orig_date_time = datetime.datetime.fromtimestamp(date)
        new_date_time = orig_date_time + datetime.timedelta(days=int(integer))
        date = new_date_time.timestamp()
        response = requests.get(url, params = payload)
        list_of_closes = response.json()["result"]
        for i in list_of_closes:
            current_price = float(i)
            should_buy, should_sell, do_nothing = algorithm.fast_forward(float(i))
            if (should_buy):
                transactions.append("bought some bit coins")
                buy_percent()
            elif (should_sell):
                transactions.append("sold some bit coins")
                sell_percent()
            elif (do_nothing):
                print("did nothing")
            response = outPutPortfolio()
            transactions.insert(0, "total value of wallet: " + str(response["result"]["total"]))
            
    return json.dumps({"status": 200})

@app.route("/set-split")
def setSplit():
    global coinPercentages
    coin = request.args.get('coin')
    percent = request.args.get('percent')
    coinPercentages[coin] = percent
    return json.dumps({"status": 200})

@app.route("/get-split")
def getSplit():
    coin = request.args.get('coin')
    percent = coinPercentages[coin]
    returned_json = {
        "speech": "Your current {0} split is {1} percent.".format(str(coin), str(percent)),
        "displayText": "Your current {0} split is {1} percent.".format(str(coin), str(percent)),
        "data": {"percent": percent},
        "source": "CryptoTrader"
    }
    response = Response(response=returned_json, status=200, mimetype="application/json")
    return response

@app.route("/get-market-data")
def getMarketData():
    global date
    coin = request.args.get('coin')
    url = backend_url + "/get_initial_closings"
    payload = None
    print(date)
    
    if (coin == "Bitcoin"):
        payload = {"timestamp": int(date), "currency": "XXBTZUSD"}
    elif (coin == "Ethereum"):
        payload = {"timestamp": int(date), "currency": "XETHZUSD"}
    elif (coin == "Litecoin"):
        payload = {"timestamp": int(date), "currency": "XLTCZUSD"}

    response = requests.get(url, params = payload)
    return json.dumps(response.json())

@app.route("/set-purchase-limit")
def setPurchaseLimit():
    global cointLimits
    coin = request.args.get('coin')
    purchaseLimit = request.args.get('setPurchaseLimit') 
    coinLimits[coin] = purchaseLimit
    return json.dumps({"status": 200})

@app.route("/get-purchase-limit")
def getPurchaseLimit():
    coin = request.args.get('coin')
    percent = coinLimits[coin]
    return json.dumps({"result": percent})

@app.route("/out-put-wallet")
def outPutWallet():
    url = backend_url + "/balance"
    payload = {"address": traderAddress}
    response = requests.get(url, params=payload)
    return json.dumps(response.json())

@app.route("/out-put-portfolio")
def outPutPortfolio():
    url = "{0}/get_money".format(backend_url)
    payload = {"address": trader_address}
    response = requests.get(url, params=payload)
    usd = response.json()["result"]

    url = "{0}/balance".format(backend_url)
    response = requests.get(url, params=payload)
    bitcoins = response.json()["final_balance"] / 1000000000

    total = usd + bitcoins * current_price

    returned_json = {
        "total": total,
        "bitcoin_balance": bitcoins,
        "bitcoin_value": bitcoins*current_price,
        "usd": usd
    }
    return ({"result": returned_json})

# resets everything
@app.route("/reset")
def reset():
    return "hello world"

@app.route("/current-prices")
def currentPrices():
    coin = request.args.get('coin')
