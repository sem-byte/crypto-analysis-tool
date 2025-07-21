# Module for derivatives market analysis
import requests
import configparser

def get_open_interest():
    """
    Fetches and returns the current Open Interest for ETHUSDT.
    """
    print("Fetching Open Interest...")
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        proxy = config['NETWORK']['proxy']

        url = "https://api.bybit.com/v5/market/open-interest"
        params = {
            "category": "linear",
            "symbol": "ETHUSDT",
            "intervalTime": "5min"
        }
        proxies = {
            "http": proxy,
            "https": proxy,
        }

        response = requests.get(url, params=params, proxies=proxies)
        data = response.json()

        if data and data['retCode'] == 0:
            open_interest = data['result']['list'][0]['openInterest']
            print(f"Current Open Interest for ETHUSDT: {open_interest}")
            return open_interest
        else:
            print(f"Error fetching Open Interest: {data}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
