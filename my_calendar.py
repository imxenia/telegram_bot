from pyicloud import PyiCloudService

# Ваши данные iCloud
icloud_username = "klyshova04@mail.ru"
icloud_password = "Rctybz2004!"

# Авторизация
api = PyiCloudService(icloud_username, icloud_password)

# Проверка двухфакторной аутентификации
if api.requires_2fa:
    print("Требуется двухфакторная аутентификация.")
    code = input("Введите код подтверждения, отправленный на ваше устройство: ")
    result = api.validate_2fa_code(code)

    if not result:
        print("Неверный код подтверждения.")
        exit(1)

# Добавление события в календарь
event_data = {
    'title': 'Запись к мастеру',  # Заголовок
    'location': 'ул. Саврасова, д. 86, ЖК Мандарин',  # Местоположение
    'starts': '2025-02-10 15:00:00',  # Дата и время начала
    'ends': '2025-02-10 16:00:00',    # Дата и время окончания
}

calendar = api.calendar
calendar.create(event_data)
print("Событие успешно добавлено в iCloud-календарь!")
