import telebot
import time

from start import start_conversation
from make import make_conversation, handle_message, callback_query, service_keyboard, added_service_keyboard
from clients import create_excel_file_if_not_exists
from price import send_price
from ask import ask_question
from notes import show_notes

bot = telebot.TeleBot("7858775434:AAFlUl5R1G6mN6o7HE5RHo7GNPp9IvRRfzQ", parse_mode=None)

create_excel_file_if_not_exists()

@bot.message_handler(commands=['start'])
def start_handler(message):
    start_conversation(bot, message)

@bot.message_handler(commands=['make'])
def make_handler(message):
    make_conversation(bot, message)

@bot.message_handler(commands=['price'])
def price_handler(message):
    send_price(bot, message)

@bot.message_handler(commands=['ask'])
def ask_handler(message):
    ask_question(bot, message)

@bot.message_handler(commands=['notes'])
def notes_handler(message):
    show_notes(bot, message)

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def message_handler(message):
    handle_message(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    callback_query(bot, call)

def start_bot_polling():
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(15)

if __name__ == "__main__":
    start_bot_polling()
