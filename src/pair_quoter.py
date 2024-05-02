from src.quoter import quoter

class pair_quoter():
    def __init__(self, trade_config, api_credentials):
        self.trade_config = trade_config
        self.api_credentials = api_credentials

    def run(self):
        spot_quoter = quoter('spot', self.trade_config, self.api_credentials)
        self.spot = spot_quoter.run()

        perpetual_quoter = quoter('perpetual', self.trade_config, self.api_credentials)
        self.perpetual = perpetual_quoter.run()

        return self

    def join(self):
        self.spot.join()
        self.perpetual.join()