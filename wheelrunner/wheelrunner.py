from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    )
import logging
import config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
logger = logging.getLogger(__name__)

job_queue = None

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

def main():
    # start Telegram bot
    updater = Updater(token=config.telegram.token)
    job_queue = updater.job_queue
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler([Filters.text], echo)
    updater.start_polling()

if __name__ == "__main__":
    main()
