# Main entry point for the Chimera V2 trading bot
from synthesizer import Synthesizer
import requests
import json

if __name__ == "__main__":
    print("Starting Chimera V2")
    session = requests.Session()
    chimera_bot = Synthesizer(session)
    trading_signal = chimera_bot.get_trading_signal(symbol="ETHUSDT")
    print(json.dumps(trading_signal, indent=4))
