import configparser
from pybit.unified_trading import HTTP
from paper_trader import PaperTrader

class TradeExecutor:
    def __init__(self, mode: str = "dry_run"):
        self.mode = mode
        if self.mode == "live":
            config = configparser.ConfigParser()
            config.read('config.ini')
            api_key = config['bybit']['api_key']
            api_secret = config['bybit']['api_secret']
            self.session = HTTP(
                testnet=False,
                api_key=api_key,
                api_secret=api_secret,
            )
        elif self.mode == "paper":
            self.paper_trader = PaperTrader()

    def open_position(self, symbol: str, side: str, qty: float, stop_loss_price: float, take_profit_price: float):
        """
        Places a market order to open a position.
        """
        if self.mode == "dry_run":
            print(f"[DRY RUN] Would have opened a {side} position for {qty} {symbol} with SL at {stop_loss_price} and TP at {take_profit_price}.")
            return
        elif self.mode == "paper":
            # For paper trading, we need the current price to open the position
            # I will add a method to get the current price later
            self.paper_trader.open_position(symbol, side, qty, 0)
            return

        try:
            self.session.place_order(
                category="linear",
                symbol=symbol,
                side=side,
                orderType="Market",
                qty=qty,
                stopLoss=str(stop_loss_price),
                takeProfit=str(take_profit_price),
            )
            print(f"Successfully opened a {side} position for {qty} {symbol}.")
        except Exception as e:
            print(f"An error occurred while opening a position: {e}")

    def close_position(self, symbol: str):
        """
        Places a market order to close the entire existing position for the given symbol.
        """
        if self.mode == "dry_run":
            print(f"[DRY RUN] Would have closed the position for {symbol}.")
            return
        elif self.mode == "paper":
            # For paper trading, we need the current price to close the position
            # I will add a method to get the current price later
            self.paper_trader.close_position(symbol, 0)
            return

        try:
            position = self.get_open_position(symbol)
            if position:
                side = "Sell" if position['side'] == "Buy" else "Buy"
                qty = position['size']
                self.session.place_order(
                    category="linear",
                    symbol=symbol,
                    side=side,
                    orderType="Market",
                    qty=qty,
                    reduce_only=True,
                )
                print(f"Successfully closed the position for {symbol}.")
            else:
                print(f"No open position for {symbol}.")
        except Exception as e:
            print(f"An error occurred while closing a position: {e}")

    def get_open_position(self, symbol: str):
        """
        Retrieves the open position for the given symbol.
        """
        if self.mode == "dry_run" or self.mode == "paper":
            return None

        try:
            response = self.session.get_positions(category="linear", symbol=symbol)
            if response and response['retCode'] == 0:
                positions = response['result']['list']
                for position in positions:
                    if float(position['size']) > 0:
                        return position
            return None
        except Exception as e:
            print(f"An error occurred while getting the open position: {e}")
            return None
