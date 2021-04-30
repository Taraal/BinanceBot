import json
import asyncio
from api import BinanceAPI

with open("logs.json") as file:
    data = json.load(file)
    api_key = data["KEY"]
    api_secret = data["SECRET"]

client = BinanceAPI(api_key, api_secret)

def extract_balance(json_data):
    
    for key in json_data.keys():
            
        try:
            return float(json_data[key])
        except KeyError:
            return 0

def get_balance():
    res = client.get_account_status()
    final_balance = []

    for coin in res["balances"]:
        if float(coin["free"]) > 0.0001:
            final_balance.append({"%s" % coin["asset"] : coin["free"]})

    with open("results.json", "w") as outfile:
        json.dump(res, outfile)

    return final_balance

asyncio.get_event_loop().run_until_complete(client.listen())