from flask import Flask
from flask import request
from flask import json

# external modules
import datetime
import json
import requests
import time

# internal modules
import algorithm
import api
import wallet

app = Flask(__name__)

blocktrail_public = api.get_blocktrail_public()
blocktrail_secret = api.get_blocktrail_secret()

trader_address = wallet.get_trader_address()
trader_passcode = wallet.get_trader_passcode()

backend_url = "https://99a5dae8.ngrok.io"

client = None
trader = None

date = None
coinPercentages = {}
coinLimits = {}

traderAddress = "2MzLGbQpMF9NEni8AqDRG4HPuUE2QHgG9nN"

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
    global date
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
            should_buy, should_sell, do_nothing = algorithm.fast_forward(float(i))
            if (should_buy):
                print("bought some bit coins")
            elif (should_sell):
                print("sold some bit coins")
            elif (do_nothing):
                print("did nothing")

    elif ("month" in duration):
        print ("test2")
    else:
        return "bad request"

@app.route("/set-split")
def setSplit():
    coin = requests.args.get('coin')
    percent = requests.args.get('percent')
    coinPercentages[coin] = percent

@app.route("/get-split")
def getSplit():
    coin = requests.args.get('coin')
    percent = coinPercentages[coin]
    return json.dumps({result: percent})

@app.route("/set-purchase-limit")
def setPurchaseLimit():
    coin = requests.args.get('coin')
    purchaseLimit = requests.args.get('setPurchaseLimit') 
    coinLimits[coin] = purchaseLimit

@app.route("/get-purchase-limit")
def getPurchaseLimit():
    coin = requests.args.get('coin')
    percent = coinLimits[coin]
    return json.dumps({result: percent})

@app.route("/out-put-wallet")
def outPutWallet():
    url = backend_url + "/balance"
    payload = {"address": traderAddress}
    response = requests.get(url, params=payload)
    return json.dumps(response)

@app.route("/out-put-portfolio")
def outPutPortfolio():
    return "hello world"
    #data = jsonify(
    #coinQuantity = #what ever the coin Quantity call thing is  ,  
    #coinTotalValue = # call coin total value put it here,
    #coinName = 
    #)

	#return jsonify(
	#speech = "you have" + coinQuantity + coinName + "worth" + coinTotalValue , 
	#displayText = speech, 
	#data = {},
	#contextOut = [],
	#source = "The Source",

	#) + data

# resets everything
@app.route("/reset")
def reset():
    return "hello world"

@app.route("/current-prices")
def currentPrices():
	coin = requests.args.get('coin')
