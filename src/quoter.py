
import threading
import time

from src.authen import send_binance_request
from src.top_orderbook import top_orderbook
from src.order_data_stream import order_data_stream

class quoter():
    def __init__(self, account_type, trade_config, api_credentials):
        self.account_type = account_type
        self.order_config = trade_config[account_type]
        self.api_credentials = api_credentials

        # Quoter's status
        self.is_quoting = True

    def get_query_string(self):
        query_str = 'recvWindow=50000'

        # Add order's info
        for key, value in self.order_config.items():
            if key == 'delay_time':
                continue
            query_str += '&' + key + '=' + str(value)

        # add price from top orderbook
        query_str += '&' + 'price' + '=' + str(self.top_orderbook.get_best_price())

        return query_str

    def send_order_request(self):
        query_str = self.get_query_string()
        resp = send_binance_request('/order', self.account_type, query_str, self.api_credentials)

        if 'msg' in resp:
            print(self.account_type.upper(), 'error:', resp['msg'])

    def update_order_status(self, order_data):
        print(order_data)
        if 'status' in order_data and self.is_quoting == True:
            self.is_quoting = order_data['status'] != 'FILLED'

            if self.is_quoting == False:
                print('STOP QUOTING', order_data['type'])

    def run(self):
        def run_on_thread(self):
            while self.is_quoting:
                self.send_order_request()

                time.sleep(self.order_config['delay_time'])

            self.top_orderbook.stop()
            self.order_data_stream.stop()

        # get top orderbook stream data
        self.top_orderbook = top_orderbook(self.account_type, self.order_config['symbol']).run()

        # order data stream
        self.order_data_stream = order_data_stream(self.account_type, self.api_credentials, self.update_order_status).run()

        # start placing order
        thread = threading.Thread(target=run_on_thread, args=(self,))
        thread.start()

        return thread