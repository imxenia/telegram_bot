import os

def send_price(bot, message):
    chat_id = message.chat.id

    price_image_path = 'price.jpg'

    if not os.path.exists(price_image_path):
        bot.send_message(chat_id, "Наш прайс-лист:"
                                  "\nКоррекция бровей - 500₽"
                                  "\nКоррекция + окрашивание - 1000₽"
                                  "\nКоррекция + окрашивание + ламинирование - 1300₽"
                                  "\nОкрашивание ресниц - 350₽"
                                  "\nУдаление пушка над верхней губой - 200₽"
                                  "\nВыезд на дом - 500₽")
        print(f"Файл {price_image_path} не найден.")
        return

    try:
        with open(price_image_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption="Вот наш прайс-лист на услуги!")
        print(f"Файл {price_image_path} успешно отправлен.")
    except Exception as e:
        bot.send_message(chat_id, "Наш прайс-лист:"
                                  "\nКоррекция бровей - 500₽"
                                  "\nКоррекция + окрашивание - 1000₽"
                                  "\nКоррекция + окрашивание + ламинирование - 1300₽"
                                  "\nОкрашивание ресниц - 350₽"
                                  "\nУдаление пушка над верхней губой - 200₽"
                                  "\nВыезд на дом - 500₽")
        print(f"Ошибка отправки прайса: {e}")
