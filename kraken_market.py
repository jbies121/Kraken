import requests
import json

# Default interval
interval = 60
# Get OHLC data of an asset since a specified Unix epoch time
def kraken_price(asset_index,time_unix,interval):
    price_check_uri = 'https://api.kraken.com/0/public/OHLC?pair='+asset_index+'&since='+str(time_unix)+'&interval='+str(interval)
    price = requests.get(price_check_uri)
    price = json.loads(price.content.decode())
    return price