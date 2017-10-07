#Sam Young
#October 7th, 2017
#Contains the functions we need for communicating with the Kraken API.

import requests
import json
import time
import krakenex

k = krakenex.API()

SECONDS_PER_DAY=86400

class  BECon(object):

    def __init__(self,serverName):
        k=krakenex.API()
        serverName=serverName

    def getClosingValues(self,buildDate,pair):
        #buildDate - Starting date to use in Epoch Time, converted by the build command.
        #pair - The pair to use. (Pair meaning Crypto->Standard Currency, ex: XXBTZUSD or XXBTZEUR). These values can be found on the Kraken website.
        buildDate=int(buildDate)
        startDate=buildDate-(34*SECONDS_PER_DAY)
        OHLCChart = k.query_public('OHLC', req={'pair': pair, 'since': str(startDate), 'interval' : 1440})
        OHLCChart = OHLCChart["result"][pair]
        closingValues=[]
        startingPosition=int((OHLCChart[-1][0]-buildDate)/86400)  
        for i in range(1,35):
            closingValues.append(OHLCChart[-startingPosition-i][3])
        return closingValues

    def getClosingValuesInRange(self, start, days, pair):
        startDate = int(start)
        days = int(days)
        #startDate = buildDate-(days*SECONDS_PER_DAY)
        buildDate = startDate+(days*SECONDS_PER_DAY)
        OHLCChart = k.query_public('OHLC', req={'pair': pair, 'since': str(startDate), 'interval' : 1440})
        OHLCChart = OHLCChart["result"][pair]
        closingValues=[]
        startingPosition=int((OHLCChart[-1][0]-buildDate)/86400)  
        for i in range(1,days+1):
            closingValues.append(OHLCChart[-startingPosition-i][3])
        return closingValues

    def walletBalance(self):
        r = requests.get(self.serverName+'/Balance/')
        return r.json()["results"]


