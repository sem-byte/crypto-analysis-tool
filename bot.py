# Main entry point for the Chimera V3 trading bot
from synthesizer import Synthesizer
import time

if __name__ == "__main__":
    print("Starting Chimera V3")
    chimera_bot = Synthesizer(mode="dry_run")

    while True:
        chimera_bot.run_cycle(symbol="ETHUSDT")
        print("Waiting for next cycle...")
        time.sleep(300)
