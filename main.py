import json
from src.pair_quoter import pair_quoter
from src.positions import positions

def load_api_credentials():
    with open('configs/api_credentials.json', 'r') as file:
        data = json.load(file)

    return data

def load_trade_config():
    with open('configs/trade_config.json', 'r') as file:
        data = json.load(file)

    return data

def main():
    trade_config = load_trade_config()
    api_credentials = load_api_credentials()

    while True:
        quoters = pair_quoter(trade_config, api_credentials)
        t1 = quoters.run()
        t1.join()

        print("PAIR QUOTER IS FINISHED, CONTINUE WITH THE OTHER ONE")

    # spot_positions = positions('spot', api_credentials)
    # t3 = spot_positions.run()
    # perpetual_positions = positions('perpetual', api_credentials)
    # t4 = perpetual_positions.run()

    # t3.join()
    # t4.join()


if __name__ == "__main__":
    main()
