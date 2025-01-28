import telebot
import time

from delete import confirm_delete, handle_delete_callback
from start import start_conversation
from make import make_conversation, handle_message, callback_query, service_keyboard, added_service_keyboard, \
    handle_book_service
from clients import save_client_data  # Import the save_client_data function from clients.py
from price import send_price
from ask import ask_question
from notes import show_notes
from database import initialize_database
from make import user_data


bot = telebot.TeleBot("7858775434:AAFlUl5R1G6mN6o7HE5RHo7GNPp9IvRRfzQ", parse_mode=None)  # Replace with your actual token

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

@bot.message_handler(commands=['delete'])
def delete_handler(message):
    confirm_delete(bot, message)

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def message_handler(message):
    chat_id = message.chat.id
    # Если пользователь не находится в процессе какого-либо действия
    if chat_id not in user_data or 'step' not in user_data[chat_id]:
        bot.send_message(chat_id, "Читать такие сообщения я пока не научился. Выберите, пожалуйста, действие из меню🤍")
    else:
        # Если пользователь находится в процессе, обрабатываем сообщение
        handle_message(bot, message)

@bot.callback_query_handler(func=lambda call: call.data not in ["delete_confirm", "delete_cancel"])
def callback_handler(call):
    if call.data == "book_service":
        handle_book_service(bot, call)
    else:
        callback_query(bot, call)

@bot.callback_query_handler(func=lambda call: call.data in ["delete_confirm", "delete_cancel"])
def delete_callback_handler(call):
    handle_delete_callback(bot, call)

def start_bot_polling():
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Ошибка: {e}. Перезапуск опроса через 15 секунд...")
            time.sleep(15)

if __name__ == "__main__":
    start_bot_polling()
