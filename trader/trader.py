from flask import Flask
from flask import request
from flask import json

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

backend_url = "https://99a5dae8.ngrok.io"

client = None
trader = None

date = None
coinPercentages = {}
coinLimits = {}

traderAddress = "2MzLGbQpMF9NEni8AqDRG4HPuUE2QHgG9nN"

@app.route("/build")
def build():
    date = requests.args.get('date')
	
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

@app.route("/fast-forward")
def fastForward():
    integer= requests.args.get('integer')
    duration= requests.args.get('duration')
    if (duration.contains('day') == true):
        print ("test1")
    elif (duration.contains('month') == true):
        print ("test2")
    else:
        return "bad request"

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
