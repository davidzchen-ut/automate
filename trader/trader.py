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

url = "https://99a5dae8.ngrok.io"

#vendor_address = wallet.get_vendor_address()
#vendor_passcode = wallet.get_vendor_passcode()

client = None
trader = None

@app.route("/")
def hello():
    return json.dumps(get_wallet_balance(vendor_address).json())

def get_wallet_balance(address):
    url = "https://api.blocktrail.com/v1/tbtc/address/{0}".format(address)
    print("url: " + url)
    payload = {"api_key": blocktrail_public}
    response = requests.get(url, params=payload)
    return response

@app.route("/api/i")
def test():
    return "test"

@app.route("/build")
def build():
	date= requests.args.get('date')
	

@app.route("/set-split")
def setSplit():
	coin = requests.args.get('coin')
	percent = requests.args.get('percent')
	#set how much of a certain coin is which percentage

@app.route("/get-split")
def getSplit():
	coin = requests.args.get('coin')
	#gets the request of a certain coin and returns the value of that coin

@app.route("/set-purchase-limit")
def setPurchaseLimit():
	coin = requests.args.get('coin')
	setPurchaseLimit = requests.args.get('setPurchaseLimit') 

@app.route("/get-purchase-limit")
def getPurchaseLimit():
	coin = requests.args.get('coin')

@app.route("/fast-forward")
def fastForward():
	integer= requests.args.get('integer')
	duration= requests.args.get('duration')

	if duration.contains('day')== true:
		print("test1")

	elif duration.contains('month')== true:
		print ("test2")
	else:
		return "Bad request"

@app.route("/out-put-wallet")
def outPutWallet():
	return #wallet ammount

@app.route("/out-put-portfolio")
def outPutPortfolio():

	data = jsonify(
	coinQuantity = #what ever the coin Quantity call thing is  ,  
	coinTotalValue = # call coin total value put it here,
	coinName = 
	)

	return jsonify(
	speech = "you have" + coinQuantity + coinName + "worth" + coinTotalValue , 
	displayText = speech, 
	data = {},
	contextOut = [],
	source = "The Source",

	) + data

@app.route("/reset")
def reset():
	#clears the system

@app.route("/current-prices")
def currentPrices():
	coin = requests.args.get('coin')



