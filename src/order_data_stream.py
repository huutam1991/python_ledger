import threading

from src.websocket_connection import websocket_channel
from src.authen import send_binance_request

order_data_stream_config = {
    'spot': {
        'url': 'stream.binance.com:9443',
        'listen_key_endpoint': '/userDataStream',
    },
    'perpetual': {
        'url': 'fstream.binance.com:443',
        'listen_key_endpoint': '/listenKey',
    },
}

class order_data_stream():
    def __init__(self, account_type, api_credentials, cb_func):
        self.config = order_data_stream_config[account_type]
        self.account_type = account_type
        self.api_credentials = api_credentials
        self.cb_func = cb_func
        self.listen_key = self.get_listen_key()

        print('self.listen_key:', self.listen_key)

    def get_listen_key(self):
        resp = send_binance_request(self.config['listen_key_endpoint'], self.account_type, "", self.api_credentials, False)
        return resp['listenKey']

    def run(self):
        def run_on_thread(self):
            self.websocket = websocket_channel(self.config['url'] + "/ws/" + self.listen_key, "", self.on_data)
            self.websocket.run()

            print("web socket order_data_stream:", self.account_type, 'stop')

        # start on thread
        thread = threading.Thread(target=run_on_thread, args=(self,))
        thread.start()

        return self

    def stop(self):
        self.websocket.stop()

    def on_data(self, data):
        order_data = {}
        # Spot
        if data['e'] == 'executionReport':
            order_data['type'] = 'SPOT'
            order_data['id'] = data['i']
            order_data['status'] = data['X']
            order_data['price'] = data['p']
            order_data['quantity'] = data['q']
            self.cb_func(order_data)
        # Perpetual
        elif data['e'] == 'ORDER_TRADE_UPDATE':
            order_data['type'] = 'PERPETUAL'
            order_data['id'] = data['o']['i']
            order_data['status'] = data['o']['X']
            order_data['price'] = data['o']['p']
            order_data['quantity'] = data['o']['q']
            self.cb_func(order_data)

        if 'status' in order_data and order_data['status'] != 'NEW':
            self.cb_func(order_data)
