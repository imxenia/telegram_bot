from telebot import types
from clients import save_client_data

user_data = {}

def make_conversation(bot, message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите, пожалуйста, своё имя")
    user_data[chat_id] = {'step': 'get_name'}

def handle_message(bot, message):
    chat_id = message.chat.id

    if chat_id in user_data:
        step = user_data[chat_id].get('step')

        if step == 'get_name':
            user_data[chat_id]['name'] = message.text
            bot.send_message(chat_id, "Введите свою фамилию")
            user_data[chat_id]['step'] = 'get_surname'

        elif step == 'get_surname':
            user_data[chat_id]['surname'] = message.text
            bot.send_message(chat_id, "Пожалуйста, выберите услугу", reply_markup=service_keyboard())
            user_data[chat_id]['step'] = 'get_service'

        elif step == 'get_day':
            user_data[chat_id]['day'] = message.text
            bot.send_message(chat_id, "Выберите удобное для Вас время")
            user_data[chat_id]['step'] = 'get_time'

        elif step == 'get_time':
            user_data[chat_id]['time'] = message.text
            bot.send_message(chat_id, "Замечательно! Остался последний шаг🌸"
                                      "\nВведите свой номер телефона без скобок, пробелов и запятых, начиная с 8☺️")
            user_data[chat_id]['step'] = 'get_phone'

        elif step == 'get_phone':
            user_data[chat_id]['phone'] = message.text
            name = user_data[chat_id]['name']
            surname = user_data[chat_id]['surname']
            service = user_data[chat_id]['service']
            added_service = user_data[chat_id].get('added_service', 'без дополнительных услуг')
            day = user_data[chat_id]['day']
            time = user_data[chat_id]['time']
            phone = user_data[chat_id]['phone']

            save_client_data(user_id=message.chat.id, name=name, surname=surname, service=service, added_service=added_service, day=day, time=time, phone=phone)


            bot.send_message(chat_id,
                             f'Отлично! Записала Вас на услугу «{service}» {day} в {time}☺️'
                             f'\nДополнительные услуги: {added_service}🌿\n'
                             f'\nСтудия находится по адресу ул. Саврасова, д. 86, ЖК Мандарин, вход со стороны водохранилища, около OZON🤍'
                             f'\nНайти студию можно по метке в Яндекс Картах: https://yandex.ru/maps/org/xeni_brows/36045696998/?ll=39.217077%2C51.611170&z=16'
                             f'\nЕсли возникнут какие-либо вопросы - задавайте, с радостью отвечу🌸\n'
                             f'\nТакже прошу ознакомиться с памяткой по уходу за бровями до и после процедуры в моей группе ВКонтакте: https://vk.com/wall-226629410_40 🥰')

            notify_admin(bot, name, surname, service, added_service, day, time, phone, chat_id)
            user_data.pop(chat_id)

def notify_admin(bot, name, surname, service, added_service, day, time, phone, chat_id):
    username = bot.get_chat(chat_id).username
    contact_info = f"https://t.me/{username}" if username else phone

    admin_chat_id = '819657611'
    admin_message = (f"Новая запись!\n"
                     f"Клиент: {name} {surname}\n"
                     f"Услуга: {service}\n"
                     f"Дополнительные услуги: {added_service}\n"
                     f"Дата: {day}\n"
                     f"Время: {time}\n"
                     f"Контакт: {contact_info}")

    bot.send_message(admin_chat_id, admin_message)

def callback_query(bot, call):
    chat_id = call.message.chat.id

    if chat_id not in user_data:
        return

    if call.data in ["correction", "correction_dye", "correction_dye_lam"]:
        if call.data == "correction":
            user_data[chat_id]['service'] = "коррекция"
        elif call.data == "correction_dye":
            user_data[chat_id]['service'] = "коррекция + окрашивание"
        elif call.data == "correction_dye_lam":
            user_data[chat_id]['service'] = "коррекция + окрашивание + ламинирование"

        bot.send_message(chat_id, "Хотели бы добавить дополнительные услуги?", reply_markup=added_service_keyboard())
        user_data[chat_id]['step'] = 'get_added_service'

    elif call.data in ["lash_tint", "lip_fuzz", "no_additional"]:
        if call.data == "lash_tint":
            user_data[chat_id]['added_service'] = "окрашивание ресниц"
        elif call.data == "lip_fuzz":
            user_data[chat_id]['added_service'] = "удаление пушка над губой"
        elif call.data == "no_additional":
            user_data[chat_id]['added_service'] = "без дополнительных услуг"

        bot.send_message(chat_id, "На какую дату хотели бы записаться?")
        user_data[chat_id]['step'] = 'get_day'

def service_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    correction = types.InlineKeyboardButton(text="Коррекция", callback_data="correction")
    correction_and_dye = types.InlineKeyboardButton(text="Коррекция + окрашивание", callback_data="correction_dye")
    correction_dye_laminate = types.InlineKeyboardButton(text="Коррекция + окрашивание + ламинирование", callback_data="correction_dye_lam")

    keyboard.add(correction)
    keyboard.add(correction_and_dye)
    keyboard.add(correction_dye_laminate)
    return keyboard

def added_service_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    lash_tint = types.InlineKeyboardButton(text="Окрашивание ресниц", callback_data="lash_tint")
    lip_fuzz_removal = types.InlineKeyboardButton(text="Удаление пушка над губой", callback_data="lip_fuzz")
    no_additional = types.InlineKeyboardButton(text="Без дополнительных услуг", callback_data="no_additional")

    keyboard.add(lash_tint)
    keyboard.add(lip_fuzz_removal)
    keyboard.add(no_additional)
    return keyboard
