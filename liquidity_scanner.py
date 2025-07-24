import configparser
import requests

class LiquidityScanner:
    def __init__(self, session):
        self.session = session
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.proxy = self.config['NETWORK']['proxy']
        self.proxies = {
            "http": self.proxy,
            "https": self.proxy,
        }

    def get_orderbook(self, symbol: str) -> dict:
        """
        Fetches the order book for the given symbol.
        """
        print(f"Fetching Order Book for {symbol}...")
        try:
            url = "https://api.bybit.com/v5/market/orderbook"
            params = {
                "category": "linear",
                "symbol": symbol,
                "limit": 10
            }

            response = self.session.get(url, params=params, proxies=self.proxies)
            data = response.json()

            if data and data['retCode'] == 0:
                return data['result']
            else:
                print(f"Error fetching Order Book: {data}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def check_for_walls(self, symbol: str) -> bool:
        """
        Checks for large liquidity walls in the order book.
        """
        orderbook = self.get_orderbook(symbol)
        if not orderbook:
            return False

        bids = orderbook.get('b', [])
        asks = orderbook.get('a', [])

        if not bids or not asks:
            return False

        avg_bid_size = sum(float(bid[1]) for bid in bids) / len(bids)
        avg_ask_size = sum(float(ask[1]) for ask in asks) / len(asks)

        for bid in bids:
            if float(bid[1]) > avg_bid_size * 15:
                print(f"Liquidity wall detected on the bid side: {bid}")
                return True

        for ask in asks:
            if float(ask[1]) > avg_ask_size * 15:
                print(f"Liquidity wall detected on the ask side: {ask}")
                return True

        return False
