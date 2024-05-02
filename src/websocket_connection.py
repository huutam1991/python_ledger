import websocket
import json

class websocket_channel():
    channel_id = 0

    def get_channel_id():
        websocket_channel.channel_id += 1
        return websocket_channel.channel_id

    def __init__(self, url, channel, on_data):
        self.url = url
        self.channel = channel
        self.on_data = on_data

    def on_message(self, ws, message):
        self.on_data(json.loads(message))

    def on_error(self, ws, error):
        print('error:', error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection:", self.url)

        if self.channel != "":
            subscribe_message = {
                "method": "SUBSCRIBE",
                "params": [
                    self.channel.lower(),
                ],
                "id": websocket_channel.get_channel_id()
            }

            ws.send(json.dumps(subscribe_message))

    def run(self):
        self.ws = websocket.WebSocketApp("wss://" + self.url,
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                )

        self.ws.run_forever()  # Set dispatcher to automatic reconnection

    def stop(self):
        self.ws.close()