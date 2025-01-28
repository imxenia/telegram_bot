from telebot import types
import sqlite3

# Подключение к базе данных
DATABASE_FILE = 'clients_data.db'

def confirm_delete(bot, message):
    chat_id = message.chat.id

    # Проверяем, есть ли запись в базе данных
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT service, day, time FROM clients WHERE user_id=?", (chat_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        service, day, time = user_data
        # Отправляем сообщение с кнопками подтверждения
        confirmation_message = (f"Вы записаны на услугу «{service}» {day} в {time}.\n"
                                "Вы уверены, что хотите отменить запись?")
        keyboard = types.InlineKeyboardMarkup()
        yes_button = types.InlineKeyboardButton(text="Да, отменить", callback_data="delete_confirm")
        no_button = types.InlineKeyboardButton(text="Нет, оставить", callback_data="delete_cancel")
        keyboard.add(yes_button, no_button)
        bot.send_message(chat_id, confirmation_message, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "У вас нет активных записей, которые можно отменить.")


def handle_delete_callback(bot, call):
    chat_id = call.message.chat.id

    if call.data == "delete_confirm":
        # Удаляем запись из базы данных
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE user_id=?", (chat_id,))
        conn.commit()
        conn.close()

        # Сообщаем пользователю об успешной отмене
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "Ваша запись была успешно отменена. Ждём вас снова!")
    elif call.data == "delete_cancel":
        # Сообщаем, что запись оставлена
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "Запись не отменена! Всё остаётся в силе!")
