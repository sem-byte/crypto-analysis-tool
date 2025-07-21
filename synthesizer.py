# The decision core of the bot
from leverage_gauge import LeverageGauge

class Synthesizer:
    def __init__(self, client):
        self.leverage_gauge = LeverageGauge(client)
        # We will add other modules here later

    def get_trading_signal(self, symbol: str) -> dict:
        """
        Generates a trading signal based on the analysis of the leverage gauge module.
        """
        market_temp = self.leverage_gauge.analyze_market_temperature(symbol)

        signal = "NEUTRAL"
        reason = "Neutral market conditions"

        if market_temp["conclusion"] == "Overheated - High risk of a long squeeze":
            signal = "STRONG SELL"
            reason = "Market is Overheated - High risk of a long squeeze"
        elif market_temp["conclusion"] == "Bearish":
            signal = "SELL"
            reason = "Market is Bearish"

        return {
            "signal": signal,
            "reason": reason,
            "source_data": {
                "funding_rate": market_temp["funding_rate"],
                "long_short_ratio": market_temp["long_short_ratio"],
                "open_interest": market_temp["open_interest"]
            }
        }
