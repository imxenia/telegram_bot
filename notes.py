import sqlite3
from telebot import types

DATABASE_FILE = 'clients_data.db'

def show_notes(bot, message):
    chat_id = message.chat.id

    # Подключение к базе данных SQLite
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        # Поиск записи о пользователе по chat_id
        cursor.execute("SELECT service, added_service, day, time FROM clients WHERE user_id=?", (chat_id,))
        user_data = cursor.fetchone()

        if user_data:
            service, added_service, day, time = user_data
            # Формирование сообщения с учётом дополнительных услуг
            if added_service:
                note_message = (f"Вы записаны на услугу «{service}» и «{added_service}» {day} в {time}🕊️\n"
                                "\nНапомню адрес и номер телефона:"
                                "\n📍ул. Саврасова, д. 86, студия «Xeni_brows»"
                                "\n☎️ +7(920)423-23-38\n"
                                "\nЕсли что-то изменится, просьба сообщить заранее🤍"
                                f"\nЖдём Вас с нетерпением!")
            else:
                note_message = (f"Вы записаны на услугу «{service}» {day} в {time}🕊️\n"
                                "\nНапомню адрес и номер телефона:"
                                "\n📍ул. Саврасова, д. 86, студия «Xeni_brows»"
                                "\n☎️ +7(920)423-23-38\n"
                                "\nЕсли что-то изменится, просьба сообщить заранее🤍"
                                f"\nЖдём Вас с нетерпением!")

            # Отправка сообщения пользователю
            bot.send_message(chat_id, note_message)
        else:
            # Если запись не найдена, отправляем сообщение с возможностью записаться
            keyboard = types.InlineKeyboardMarkup()
            book_button = types.InlineKeyboardButton(text="Записаться", callback_data="book_service")
            keyboard.add(book_button)

            bot.send_message(chat_id, "У вас пока нет записей, но мы можем это исправить😇", reply_markup=keyboard)

    except Exception as e:
        # Обработка ошибок
        print(f"Произошла ошибка при получении записей: {e}")
    finally:
        # Закрытие соединения с базой данных
        conn.close()

