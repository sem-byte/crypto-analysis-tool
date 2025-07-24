import pandas as pd
import pandas_ta as ta

class PsychologicalScanner:
    def __init__(self, session):
        self.session = session

    def get_historical_data(self, symbol: str, interval: str = "60", limit: int = 200, ohlcv_df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Fetches historical kline (candlestick) data for the given symbol.
        If ohlcv_df is provided, it will be used instead of fetching new data.
        """
        if ohlcv_df is not None:
            return ohlcv_df

        print(f"Fetching historical data for {symbol}...")
        try:
            # Note: This is a placeholder for the actual API call.
            # You would need to replace this with the correct Bybit API call to fetch OHLCV data.
            # The data should be returned as a pandas DataFrame with columns:
            # ['open', 'high', 'low', 'close', 'volume']
            data = {
                'open': [100, 110, 120, 115, 125],
                'high': [115, 125, 130, 120, 135],
                'low': [95, 105, 115, 110, 120],
                'close': [110, 120, 125, 118, 130],
                'volume': [1000, 1500, 1200, 1800, 2000]
            }
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"An error occurred while fetching historical data: {e}")
            return pd.DataFrame()

    def detect_patterns(self, ohlcv_df: pd.DataFrame) -> list:
        """
        Detects chart patterns using the pandas-ta library.
        """
        if ohlcv_df.empty:
            return []

        patterns = []
        # Use pandas-ta to detect patterns
        ohlcv_df.ta.cdl_2crows(append=True)
        ohlcv_df.ta.cdl_3blackcrows(append=True)
        ohlcv_df.ta.cdl_3inside(append=True)
        # ... add more pattern detection as needed

        # Check the last few candles for detected patterns
        for index, row in ohlcv_df.tail().iterrows():
            if row.get('CDL_2CROWS') == -100:
                patterns.append('BEARISH_2CROWS')
            if row.get('CDL_3BLACKCROWS') == -100:
                patterns.append('BEARISH_3BLACKCROWS')
            if row.get('CDL_3INSIDE') == -100:
                patterns.append('BEARISH_3INSIDE')
        return patterns

    def get_atr(self, ohlcv_df: pd.DataFrame) -> float:
        """
        Calculates the ATR (Average True Range) value from historical data.
        """
        if ohlcv_df.empty:
            return 0.0

        atr = ohlcv_df.ta.atr()
        return atr.iloc[-1]

    def get_market_regime(self, symbol: str) -> str:
        """
        Determines the market regime (Bullish/Bearish) based on the 200-period EMA.
        """
        ohlcv_df = self.get_historical_data(symbol, interval="240", limit=200) # 4-hour data
        if ohlcv_df.empty:
            return "Neutral"

        ema = ohlcv_df.ta.ema(length=200)
        last_close = ohlcv_df['close'].iloc[-1]

        if last_close > ema.iloc[-1]:
            return "Bullish"
        else:
            return "Bearish"

    def analyze_chart_psychology(self, symbol: str) -> int:
        """
        Analyzes the chart psychology and returns a score from -10 to +10.
        """
        ohlcv_df = self.get_historical_data(symbol)
        detected_patterns = self.detect_patterns(ohlcv_df)

        score = 0
        if any("BULLISH" in p for p in detected_patterns):
            score = -6
        elif any("BEARISH" in p for p in detected_patterns):
            score = 6

        return score
