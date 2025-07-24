# The decision core of the bot
from leverage_gauge import LeverageGauge
from flow_guardian import FlowGuardian
from narrative_analyzer import NarrativeAnalyzer
from psychological_scanner import PsychologicalScanner
from trade_executor import TradeExecutor

from liquidity_scanner import LiquidityScanner

class Synthesizer:
    def __init__(self, mode: str = "dry_run"):
        self.leverage_gauge = LeverageGauge(None) # No session needed for now
        self.flow_guardian = FlowGuardian(None) # No session needed for now
        self.narrative_analyzer = NarrativeAnalyzer()
        self.psy_scanner = PsychologicalScanner(None) # No session needed for now
        self.liquidity_scanner = LiquidityScanner(None) # No session needed for now
        self.executor = TradeExecutor(mode=mode)
        self.weights = {
            "leverage": 1.5,
            "flow": 1.2,
            "psy": 0.8,
            "narrative": 0.5
        }

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
        # Placeholder for narrative score
        narrative_score = 0

        # Step 3: Sum Scores with Weights
        total_score = (leverage_score * self.weights['leverage'] +
                       flow_score * self.weights['flow'] +
                       psychology_score * self.weights['psy'] +
                       narrative_score * self.weights['narrative'])

        # Liquidity Filter
        if self.liquidity_scanner.check_for_walls(symbol):
            print("Action blocked by a large liquidity wall.")
            self.executor.close_position(symbol) # Close any open positions
            return

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

            risk_per_trade = 0.01
            balance = self.executor.paper_trader.balance if self.executor.mode == 'paper' else 1000 # Placeholder for live balance
            risk_amount_usd = balance * risk_per_trade

            if signal == "STRONG BUY":
                stop_loss_price = last_close - 2 * atr
                take_profit_price = last_close + 4 * atr # 2:1 R/R
                stop_loss_distance_usd = last_close - stop_loss_price
                trade_qty = risk_amount_usd / stop_loss_distance_usd if stop_loss_distance_usd > 0 else 0
                if trade_qty > 0:
                    self.executor.open_position(symbol, "Buy", trade_qty, stop_loss_price, take_profit_price)
            elif signal == "STRONG SELL":
                stop_loss_price = last_close + 2 * atr
                take_profit_price = last_close - 4 * atr # 2:1 R/R
                stop_loss_distance_usd = stop_loss_price - last_close
                trade_qty = risk_amount_usd / stop_loss_distance_usd if stop_loss_distance_usd > 0 else 0
                if trade_qty > 0:
                    self.executor.open_position(symbol, "Sell", trade_qty, stop_loss_price, take_profit_price)
        else:
            # Close any open positions if the signal is neutral
            self.executor.close_position(symbol)

    def manage_open_position(self, symbol):
        print("Logic for managing open position (e.g., trailing stop) would go here.")
