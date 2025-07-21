# The decision core of the bot
from leverage_gauge import LeverageGauge
from flow_guardian import FlowGuardian
from narrative_analyzer import NarrativeAnalyzer

class Synthesizer:
    def __init__(self, client):
        self.leverage_gauge = LeverageGauge(client)
        self.flow_guardian = FlowGuardian(client)
        self.narrative_analyzer = NarrativeAnalyzer()
        # We will add other modules here later

    def get_trading_signal(self, symbol: str) -> dict:
        """
        Generates a trading signal based on the analysis of the leverage gauge, flow guardian, and narrative analyzer modules.
        """
        market_temp = self.leverage_gauge.analyze_market_temperature(symbol)
        spot_flow = self.flow_guardian.analyze_spot_flow(symbol)
        narrative = self.narrative_analyzer.analyze_market_narrative(symbol)

        signal = "NEUTRAL"
        reason = "Neutral market conditions"

        # Contrarian SELL
        if (market_temp["conclusion"] == "Overheated - High risk of a long squeeze" and
                spot_flow["conclusion"] == "Whales are selling" and
                narrative["conclusion"] == "Extreme Greed / Euphoria"):
            signal = "STRONG SELL"
            reason = "Market is Overheated, Whales are selling, and sentiment is euphoric"

        # Contrarian BUY
        elif (market_temp["conclusion"] != "Overheated - High risk of a long squeeze" and
                spot_flow["conclusion"] == "Whales are buying" and
                narrative["conclusion"] == "Extreme Fear / Capitulation"):
            signal = "STRONG BUY"
            reason = "Whales are buying and sentiment is fearful"

        # Weaker signals
        elif market_temp["conclusion"] == "Overheated - High risk of a long squeeze":
            signal = "SELL"
            reason = "Market is Overheated"
        elif spot_flow["conclusion"] == "Whales are selling":
            signal = "SELL"
            reason = "Whales are selling"
        elif market_temp["conclusion"] == "Bearish":
            signal = "SELL"
            reason = "Market is Bearish"

        return {
            "signal": signal,
            "reason": reason,
            "source_data": {
                "leverage_gauge": market_temp,
                "flow_guardian": spot_flow,
                "narrative_analyzer": narrative
            }
        }
