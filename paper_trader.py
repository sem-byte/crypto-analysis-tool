class PaperTrader:
    def __init__(self):
        self.balance = 1000.0
        self.position = None
        self.trade_log = []

    def open_position(self, symbol, side, qty, price):
        """
        Simulates opening a trade.
        """
        if self.position:
            print("Already in a position.")
            return

        margin = qty * price * 0.1 # 10x leverage
        if self.balance < margin:
            print("Insufficient balance.")
            return

        self.position = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "entry_price": price
        }
        print(f"Opened a {side} position for {qty} {symbol} at {price}.")

    def close_position(self, symbol, price):
        """
        Simulates closing a trade.
        """
        if not self.position or self.position['symbol'] != symbol:
            print("No open position for this symbol.")
            return

        pnl = 0
        if self.position['side'] == 'Buy':
            pnl = (price - self.position['entry_price']) * self.position['qty']
        else:
            pnl = (self.position['entry_price'] - price) * self.position['qty']

        self.balance += pnl
        self.log_trade(self.position['symbol'], self.position['side'], self.position['qty'], self.position['entry_price'], price, pnl)
        self.position = None
        print(f"Closed position for {symbol} at {price}. PnL: {pnl:.2f}. New balance: {self.balance:.2f}")

    def log_trade(self, symbol, side, qty, entry_price, exit_price, pnl):
        """
        Logs a trade to the trade log.
        """
        self.trade_log.append({
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl": pnl
        })
