import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

class TelegramController:
    def __init__(self, bot_instance, token, chat_id):
        self.bot_instance = bot_instance
        self.application = Application.builder().token(token).build()
        self.chat_id = chat_id

        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("close", self.close))

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends the current status of the bot."""
        if self.bot_instance.executor.mode == 'paper':
            balance = self.bot_instance.executor.paper_trader.balance
            position = self.bot_instance.executor.paper_trader.position
            await update.message.reply_text(f"Balance: {balance:.2f}\nPosition: {position}")
        else:
            await update.message.reply_text("Status only available in paper trading mode.")

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Stops the bot gracefully."""
        await update.message.reply_text("Stopping the bot...")
        # This is a placeholder for the actual stop logic.
        # In a real application, you would use a global flag or event to signal the main loop to exit.
        print("Received /stop command. The bot should stop gracefully.")

    async def close(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Closes the current position."""
        await update.message.reply_text("Closing position...")
        self.bot_instance.executor.close_position("ETHUSDT")

    def run(self):
        """Runs the Telegram bot in a separate thread."""
        thread = threading.Thread(target=self.application.run_polling)
        thread.start()
