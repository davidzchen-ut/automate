import krakenComm

backend = krakenComm.BECon('http://99a5dae8.ngrok.io/')

print(backend.getClosingValues('1451606400','XXBTZUSD'))
print(backend.walletBalance("2NBjbqj8WFkctwummc22gwTTTEUb5t7bg8M"))
