# Module for spot market analysis
import requests
import configparser

class FlowGuardian:
    def __init__(self, session):
        self.session = session
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.proxy = self.config['NETWORK']['proxy']
        self.proxies = {
            "http": self.proxy,
            "https": self.proxy,
        }

    def get_net_crypto_flow(self, symbol: str) -> dict:
        """
        Fetches data for the "Net Crypto Flow" chart.

        NOTE: This is a placeholder function that returns mock data.
        The Bybit API does not currently provide a direct endpoint for this data.
        """
        print(f"Fetching Net Crypto Flow for {symbol}...")
        # Mock data representing net inflows/outflows over time
        return {"net_flow": [100, -50, 200, -150, 300]}

    def get_taker_volume_distribution(self, symbol: str) -> dict:
        """
        Fetches the data from the pie chart showing the distribution of taker buy/sell volume.

        NOTE: This is a placeholder function that returns mock data.
        The Bybit API does not currently provide a direct endpoint for this data.
        """
        print(f"Fetching Taker Volume Distribution for {symbol}...")
        # Mock data representing the distribution of taker buy/sell volume
        return {
            'large_buys': 0.15,
            'large_sells': 0.20,
            'medium_buys': 0.25,
            'medium_sells': 0.10,
            'small_buys': 0.15,
            'small_sells': 0.15,
        }

    def get_ticker_info(self, symbol: str) -> dict:
        """
        Fetches the ticker information for the given symbol.
        """
        print(f"Fetching Ticker Info for {symbol}...")
        try:
            url = "https://api.bybit.com/v5/market/tickers"
            params = {
                "category": "linear",
                "symbol": symbol,
            }

            response = self.session.get(url, params=params, proxies=self.proxies)
            data = response.json()

            if data and data['retCode'] == 0:
                return data['result']['list'][0]
            else:
                print(f"Error fetching Ticker Info: {data}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def analyze_spot_flow(self, symbol: str) -> int:
        """
        Analyzes the spot market flow and returns a score from -10 to +10.
        """
        ticker_info = self.get_ticker_info(symbol)

        score = 0
        if ticker_info:
            price_24h_change = float(ticker_info['price24hPcnt'])
            if price_24h_change < -0.05:
                score = -9
            elif price_24h_change < 0:
                score = -2
            elif price_24h_change > 0.05:
                score = 9
            elif price_24h_change > 0:
                score = 2
        return score
