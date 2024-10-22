def ask_question(bot, message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Что Вас заинтересовало?")
    bot.register_next_step_handler(message, process_question, bot)


def process_question(message, bot):
    chat_id = message.chat.id
    user_question = message.text

    username = message.from_user.username
    if username:
        user_link = f"https://t.me/{username}"
        send_admin_notification(bot, chat_id, user_question, user_link)
    else:
        bot.send_message(chat_id, "Ваш аккаунт скрыт для других пользователей. Пожалуйста, укажите свой номер телефона для связи🌸")
        bot.register_next_step_handler(message, process_phone_number, bot, user_question)


def process_phone_number(message, bot, user_question):
    chat_id = message.chat.id
    user_phone = message.text

    send_admin_notification(bot, chat_id, user_question, user_phone)


def send_admin_notification(bot, chat_id, user_question, contact_info):
    admin_chat_id = '819657611'
    admin_message = (f"Необходимо связаться с клиентом!\n"
                     f"Вопрос: {user_question}\n"
                     f"Контактная информация: {contact_info}")

    bot.send_message(admin_chat_id, admin_message)

    bot.send_message(chat_id, "Спасибо за проявленный интерес к нашей студии! Свяжемся с Вами в самые кратчайшие сроки😌")
