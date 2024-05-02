from src.websocket_connection import websocket_channel
import threading

orderbook_config = {
    'spot': {
        'url': 'stream.binance.com:9443/ws',
        'update_speed': '1000ms',
        'ask_field': 'asks',
        'bid_field': 'bids',
    },
    'perpetual': {
        'url': 'fstream.binance.com:443/ws',
        'update_speed': '500ms',
        'ask_field': 'a',
        'bid_field': 'b',
    },
}

class top_orderbook():
    def __init__(self, account_type, symbol):
        self.account_type = account_type
        self.symbol = symbol
        self.ask_field = orderbook_config[self.account_type]['ask_field']
        self.bid_field = orderbook_config[self.account_type]['bid_field']

    def run(self):
        def run_on_thread(self):
            self.websocket = websocket_channel(orderbook_config[self.account_type]['url'], self.symbol + '@depth5@' + orderbook_config[self.account_type]['update_speed'], self.on_data)
            self.websocket.run()

            print("web socket top_orderbook:", self.account_type, 'stop')

        # start order book
        thread = threading.Thread(target=run_on_thread, args=(self,))
        thread.start()

        return self

    def stop(self):
        self.websocket.stop()

    def on_data(self, data):
        if self.ask_field in data and self.bid_field in data:
            self.top_ask = data[self.ask_field][0][0]
            self.top_bid = data[self.bid_field][0][0]

    def get_best_price(self):
        if hasattr(self, 'top_ask') and hasattr(self, 'top_bid'):
            if self.account_type == 'spot':
                return self.top_bid
            else:
                return self.top_ask
        else:
            return 0.0