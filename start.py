def start_conversation(bot, message):
    chat_id = message.chat.id

    bot.send_message(chat_id, "Доброго времени суток!🌿 \nВыберите интересующий Вас запрос в меню☺️")
