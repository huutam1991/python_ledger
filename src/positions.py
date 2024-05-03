import time
import requests
import threading
import json
from datetime import datetime

from src.authen import hmac_hashing

url_spot      = "https://api.binance.com/api/v3/account"
url_perpetual = "https://fapi.binance.com/fapi/v2/account"

class positions():
    def __init__(self, account_type, api_credentials, symbol):
        self.account_type = account_type
        self.url = url_spot if account_type == 'spot' else url_perpetual
        self.api_credentials = api_credentials
        self.symbol = symbol

        self.is_fetching = True

    def get_query_string(self):
        query_str = 'recvWindow=50000'

        # Add timestamp + signature
        timestamp = int(datetime.now().timestamp() * 1000)
        query_str = query_str + '&timestamp=' + str(timestamp)
        signature = hmac_hashing(self.api_credentials['api_secret'], query_str)
        query_str += '&signature=' + signature

        return query_str

    def send_order_request(self):
        endpoint = self.url + '?' + self.get_query_string()
        headers = {
            "X-MBX-APIKEY": self.api_credentials['api_key']
        }

        response = requests.get(endpoint, headers=headers)
        data = json.loads(response.text)
        current_positions = self.format_positions(data)
        # print('current_positions:', current_positions)

        if self.symbol in current_positions:
            print('POSITION:', self.account_type, self.symbol, ': ', current_positions[self.symbol])
        else:
            symbol = self.symbol.replace('USDT', '')
            if symbol in current_positions:
                print('POSITION:', self.account_type, self.symbol, ': ', current_positions[symbol])

    def format_positions(self, data):
        res = {}
        data = data['balances'] if self.account_type == 'spot' else data['assets']
        for coin in data:
            res[coin['asset']] = coin

        return res

    def stop(self):
        self.is_fetching = False

    def run(self):
        def run_on_thread(self):
            while self.is_fetching:
                self.send_order_request()

                time.sleep(1.0)

        thread = threading.Thread(target=run_on_thread, args=(self,))
        thread.start()

        return thread