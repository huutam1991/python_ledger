import hmac
import hashlib
from datetime import datetime
import requests
import json

url_spot      = "https://api.binance.com/api/v3"
url_perpetual = "https://fapi.binance.com/fapi/v1"

def hmac_hashing(api_secret, payload):
    m = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256)
    return m.hexdigest()

def send_binance_request(endpoint, account_type, query_str, api_credentials, need_signing = True):
    # Add timestamp + signature
    if need_signing == True:
        timestamp = int(datetime.now().timestamp() * 1000)
        query_str += "&" if query_str != "" else ""
        query_str += 'timestamp=' + str(timestamp)
        signature = hmac_hashing(api_credentials['api_secret'], query_str)
        query_str += '&signature=' + signature

    url = url_spot if account_type == 'spot' else url_perpetual
    url += endpoint + '?' + query_str

    headers = {
        "X-MBX-APIKEY": api_credentials['api_key']
    }

    response_str = requests.post(url, headers=headers).text
    return json.loads(response_str)