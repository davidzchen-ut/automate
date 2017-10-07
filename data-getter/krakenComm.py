#Sam Young
#October 7th, 2017
#Contains the functions we need for communicating with the Kraken API.

import requests
import json
#import Flask
import time
import krakenex

k = krakenex.API()

secsPerDay=86400

def getClosingValues(buildDate,pair):
    #buildDate - Starting date to use in Epoch Time, converted by the build command.
    #pair - The pair to use. (Pair meaning Crypto->Standard Currency, ex: XXBTZUSD or XXBTZEUR). These values can be found on the Kraken website.
    startDate=buildDate-(34*secsPerDay)
    OHLCChart = k.query_public('OHLC', req={'pair': pair, 'since': str(startDate), 'interval' : 1440})
    OHLCChart = OHLCChart["result"][pair]
    closingValues=[]
    startingPosition=OHLCChart[-1][0]-buildDate
    startingPosition/=86400
    startingPosition=int(startingPosition)
    for i in range(1,35):
        closingValues.append(OHLCChart[-startingPosition-i][3])
    return closingValues

def walletBalance():
    k.load_key('kraken.key')
    return k.query_private('Balance')


#getClosingValues(1451606400,'XXBTZUSD') #January 1st 2016, BTZ to USD
#walletBalance()

#while 1:
#    userInput=input("Enter command: ").split(" ")
#    if userInput[0]=="closingValues":
#        print(getClosingValues(int(userInput[1]),userInput[2]))
#    elif userInput[0]=="balance":
#        print(walletBalance())
