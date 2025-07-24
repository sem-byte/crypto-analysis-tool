import pandas as pd
from synthesizer import Synthesizer
from psychological_scanner import PsychologicalScanner
import os

def download_historical_data(symbol, interval, limit):
    """
    Downloads historical data and saves it to a CSV file.
    """
    scanner = PsychologicalScanner(None)
    df = scanner.get_historical_data(symbol, interval, limit)
    filepath = f"historical_data_{symbol}_{interval}.csv"
    df.to_csv(filepath, index=False)
    return filepath

def run_backtest(filepath):
    """
    Runs a backtest on the given historical data.
    """
    df = pd.read_csv(filepath)
    chimera_bot = Synthesizer(mode="paper")

    for index, row in df.iterrows():
        # This is a simplified approach. In a real backtester, you would need to
        # feed the data to each module in a more sophisticated way.
        # For now, we will just call the run_cycle method.
        chimera_bot.run_cycle("ETHUSDT")

    # Print the trade log
    print("Trade Log:")
    for trade in chimera_bot.executor.paper_trader.trade_log:
        print(trade)

    # Print the final balance
    print(f"Final Balance: {chimera_bot.executor.paper_trader.balance:.2f}")

if __name__ == "__main__":
    # Download data if it doesn't exist
    filepath = "historical_data_ETHUSDT_60.csv"
    if not os.path.exists(filepath):
        filepath = download_historical_data("ETHUSDT", "60", 200)

    run_backtest(filepath)
