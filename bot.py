# Main entry point for the Chimera V4 trading bot
from synthesizer import Synthesizer
from telegram_controller import TelegramController
import time
import configparser

if __name__ == "__main__":
    print("Starting Chimera V4")

    config = configparser.ConfigParser()
    config.read('config.ini')
    telegram_token = config['telegram']['token']
    chat_id = config['telegram']['chat_id']

    chimera_bot = Synthesizer(mode="paper")
    telegram_controller = TelegramController(chimera_bot, telegram_token, chat_id)
    telegram_controller.run()

    while True:
        chimera_bot.run_cycle(symbol="ETHUSDT")
        if chimera_bot.executor.get_open_position(symbol="ETHUSDT"):
            chimera_bot.manage_open_position(symbol="ETHUSDT")
        print("Waiting for next cycle...")
        time.sleep(300)
