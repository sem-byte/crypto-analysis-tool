# Main entry point for the Chimera V2 trading bot
from leverage_gauge import get_open_interest

if __name__ == "__main__":
    print("Starting Chimera V2")
    get_open_interest()
