import requests
import hmac
import json
import base64
import hashlib
import datetime, time
import config

gemini_api_key = config.gemini_api_key
gemini_api_secret = config.gemini_api_secret
base_url = "https://api.gemini.com"

def Auth(payload):
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

    request_headers = {
        'Content-Type': "text/plain",
        'Content-Length': "0",
        'X-GEMINI-APIKEY': gemini_api_key,
        'X-GEMINI-PAYLOAD': b64,
        'X-GEMINI-SIGNATURE': signature,
        'Cache-Control': "no-cache"
    }

    return request_headers

def getPaymentMethods():
    t = datetime.datetime.now()
    payload_nonce = str(int(time.mktime(t.timetuple())*1000))
    endpoint = "/v1/payments/methods"
    payload = {"request": endpoint, "account": "primary", "nonce": payload_nonce}
    print(requests.post(base_url+endpoint, headers=Auth(payload)).json())

def placeOrder(coin_pair, amount, price):
    t = datetime.datetime.now()
    payload_nonce = str(int(time.mktime(t.timetuple())*1000))
    endpoint = "/v1/order/new"
    payload = {
        "request": endpoint,
        "nonce": payload_nonce,
        "symbol": coin_pair,
        "amount": amount,
        "price": price,
        "side": "buy",
        "type": "exchange limit",
    }
    print(requests.post(base_url+endpoint, headers=Auth(payload)).json())


coin_pair = "ethgbp"
response = requests.get("https://api.gemini.com/v1/pubticker/"+coin_pair).json()

price = float(response['ask'])
print("ask price:   "+str(price))

maker_price = round(price+(price/100*0.01), 2)
print("maker price: "+str(maker_price))
#placeOrder(coin_pair, "0.34", maker_price)

