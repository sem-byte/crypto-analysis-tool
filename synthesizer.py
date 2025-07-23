# The decision core of the bot
from leverage_gauge import LeverageGauge
from flow_guardian import FlowGuardian
from narrative_analyzer import NarrativeAnalyzer
from psychological_scanner import PsychologicalScanner
from trade_executor import TradeExecutor

class Synthesizer:
    def __init__(self, mode: str = "dry_run"):
        self.leverage_gauge = LeverageGauge(None) # No session needed for now
        self.flow_guardian = FlowGuardian(None) # No session needed for now
        self.narrative_analyzer = NarrativeAnalyzer()
        self.psy_scanner = PsychologicalScanner(None) # No session needed for now
        self.executor = TradeExecutor(mode=mode)

    def run_cycle(self, symbol: str):
        """
        Runs a single trading cycle.
        """
        # Step 1: Check Regime
        regime = self.psy_scanner.get_market_regime(symbol)

        # Step 2: Calculate Scores
        leverage_score = self.leverage_gauge.analyze_market_temperature(symbol)
        flow_score = self.flow_guardian.analyze_spot_flow(symbol)
        psychology_score = self.psy_scanner.analyze_chart_psychology(symbol)

        # Step 3: Sum Scores
        total_score = leverage_score + flow_score + psychology_score

        # Step 4: Make Decision
        signal = "NEUTRAL"
        if regime == "Bullish" and total_score > 15:
            signal = "STRONG BUY"
        elif regime == "Bearish" and total_score < -15:
            signal = "STRONG SELL"

        # Step 5: Execute with Risk Management
        if signal != "NEUTRAL":
            ohlcv_df = self.psy_scanner.get_historical_data(symbol)
            atr = self.psy_scanner.get_atr(ohlcv_df)
            last_close = ohlcv_df['close'].iloc[-1]

            if signal == "STRONG BUY":
                stop_loss_price = last_close - 2 * atr
                take_profit_price = last_close + 4 * atr # 2:1 R/R
                self.executor.open_position(symbol, "Buy", 0.01, stop_loss_price, take_profit_price)
            elif signal == "STRONG SELL":
                stop_loss_price = last_close + 2 * atr
                take_profit_price = last_close - 4 * atr # 2:1 R/R
                self.executor.open_position(symbol, "Sell", 0.01, stop_loss_price, take_profit_price)
        else:
            # Close any open positions if the signal is neutral
            self.executor.close_position(symbol)
