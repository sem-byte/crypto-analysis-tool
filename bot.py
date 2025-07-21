# Main entry point for the Chimera V2 trading bot
from leverage_gauge import LeverageGauge
import requests
import json

if __name__ == "__main__":
    print("Starting Chimera V2")
    session = requests.Session()
    gauge = LeverageGauge(session)
    market_temp = gauge.analyze_market_temperature("ETHUSDT")
    print(json.dumps(market_temp, indent=4))
