from telegram import (
    ForceReply,
    ReplyKeyboardMarkup,
    KeyboardButton,
    )
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    )
import logging
import config
from lib.geocoding import geocoder
from lib.weather import Weather
from models.user import User

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
logger = logging.getLogger(__name__)

START, AWAIT_PLACE, AWAIT_TIME_OF_DAY, AWAIT_FREQUENCY, SLEEPING = range(5)
MORNINGS = 'Mornings'
EVENINGS = 'Evenings'
NO_PREFERENCE = 'Both'
TIME_OF_DAY_OPTIONS = (MORNINGS, EVENINGS, NO_PREFERENCE)

state = dict()
users = dict()

def start(bot, update):
    chat_id = update.message.chat_id

    state[chat_id] = AWAIT_PLACE
    bot.sendMessage(
        chat_id=chat_id,
        text="Hey! I'm WheelRunner and I can help you plan rides.")
    bot.sendMessage(
        chat_id=chat_id,
        text="I've got a few questions. First, could you tell me where you're based?")


def reply(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text
    chat_state = state.get(chat_id, START)
    user = users.get(user_id) 
    if user is None:
        users[user_id] = user = User()

    if chat_state == AWAIT_PLACE:
        state[chat_id] = AWAIT_TIME_OF_DAY

        user.place = geocoder.get_place(text)
        bot.sendMessage(
            chat_id=chat_id,
            text="Cool! I've recorded your location as {0}.".format(user.place))

        # ask time
        reply_markup = ReplyKeyboardMarkup(
            [map(KeyboardButton, TIME_OF_DAY_OPTIONS)],
            one_time_keyboard=True)
        bot.sendMessage(chat_id=chat_id, text="When do you go for rides?", reply_markup=reply_markup)
    elif chat_state == AWAIT_TIME_OF_DAY:
        state[chat_id] = AWAIT_FREQUENCY

        user.can_ride_morning = text in (MORNINGS, NO_PREFERENCE)
        user.can_ride_evening = text in (EVENINGS, NO_PREFERENCE)

        # ask frequency
        reply_markup = ReplyKeyboardMarkup(
            [map(KeyboardButton, map(str, range(1, 8)))],
            one_time_keyboard=True)
        bot.sendMessage(chat_id=chat_id, text="How many rides do you do per week?", reply_markup=reply_markup)
    elif chat_state == AWAIT_TIME_OF_DAY:
        state[chat_id] = SLEEPING

        user.frequency = float(text)
        weather = Weather()
        day, score, weather_score = weather.suggest_time(user) 
        bot.sendMessage(chat_id=chat_id, text="I'd suggest a ride on {0}".format(day.strftime('%A %x')))


def main():
    # start Telegram bot
    updater = Updater(token=config.telegram['token'])
    job_queue = updater.job_queue
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    reply_handler = MessageHandler([Filters.text], reply)
    dispatcher.add_handler(reply_handler)

    updater.start_polling()

if __name__ == "__main__":
    main()
