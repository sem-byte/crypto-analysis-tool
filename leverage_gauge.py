# Module for derivatives market analysis
import requests
import configparser

class LeverageGauge:
    def __init__(self, session):
        self.session = session
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.proxy = self.config['NETWORK']['proxy']
        self.proxies = {
            "http": self.proxy,
            "https": self.proxy,
        }

    def get_open_interest(self, symbol: str):
        """
        Fetches and returns the current Open Interest for the given symbol.
        """
        print(f"Fetching Open Interest for {symbol}...")
        try:
            url = "https://api.bybit.com/v5/market/open-interest"
            params = {
                "category": "linear",
                "symbol": symbol,
                "intervalTime": "5min"
            }

            response = self.session.get(url, params=params, proxies=self.proxies)
            data = response.json()

            if data and data['retCode'] == 0:
                open_interest = data['result']['list'][0]['openInterest']
                print(f"Current Open Interest for {symbol}: {open_interest}")
                return float(open_interest)
            else:
                print(f"Error fetching Open Interest: {data}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_funding_rate(self, symbol: str) -> float:
        """
        Fetches the latest funding rate for the given symbol and returns it as a float.
        """
        print(f"Fetching Funding Rate for {symbol}...")
        try:
            url = "https://api.bybit.com/v5/market/funding/history"
            params = {
                "category": "linear",
                "symbol": symbol,
                "limit": 1
            }

            response = self.session.get(url, params=params, proxies=self.proxies)
            data = response.json()

            if data and data['retCode'] == 0:
                funding_rate = data['result']['list'][0]['fundingRate']
                print(f"Current Funding Rate for {symbol}: {funding_rate}")
                return float(funding_rate)
            else:
                print(f"Error fetching Funding Rate: {data}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_long_short_ratio(self, symbol: str) -> float:
        """
        Fetches the global long/short account ratio for the given symbol and returns it as a float.
        """
        print(f"Fetching Long/Short Ratio for {symbol}...")
        try:
            url = "https://api.bybit.com/v5/market/account-ratio"
            params = {
                "category": "linear",
                "symbol": symbol,
                "period": "5min",
                "limit": 1
            }

            response = self.session.get(url, params=params, proxies=self.proxies)
            data = response.json()

            if data and data['retCode'] == 0:
                long_short_ratio = data['result']['list'][0]['buyRatio']
                print(f"Current Long/Short Ratio for {symbol}: {long_short_ratio}")
                return float(long_short_ratio)
            else:
                print(f"Error fetching Long/Short Ratio: {data}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_recent_liquidations(self, symbol: str, limit: int = 200) -> list:
        """
        Fetches the most recent liquidation orders.
        """
        print(f"Fetching Recent Liquidations for {symbol}...")
        try:
            url = "https://api.bybit.com/v5/market/recent-trade"
            params = {
                "category": "linear",
                "symbol": symbol,
                "limit": limit
            }

            response = self.session.get(url, params=params, proxies=self.proxies)
            data = response.json()

            if data and data['retCode'] == 0:
                # This is not a direct liquidation feed, so we are just returning the raw trade data for now.
                # In a real application, we would need to filter this data for liquidations.
                return data['result']['list']
            else:
                print(f"Error fetching Recent Liquidations: {data}")
                return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def analyze_market_temperature(self, symbol: str) -> dict:
        """
        Analyzes the market temperature by fetching and analyzing various metrics.
        """
        funding_rate = self.get_funding_rate(symbol)
        long_short_ratio = self.get_long_short_ratio(symbol)
        open_interest = self.get_open_interest(symbol)

        conclusion = "Neutral"
        if funding_rate is not None and long_short_ratio is not None:
            if funding_rate > 0.0002 and long_short_ratio > 1.5:
                conclusion = "Overheated - High risk of a long squeeze"
            elif funding_rate < 0:
                conclusion = "Bearish"

        return {
            "funding_rate": funding_rate,
            "long_short_ratio": long_short_ratio,
            "open_interest": open_interest,
            "conclusion": conclusion
        }
