from flask import Flask

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
