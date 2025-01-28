import os
from datetime import datetime

from pyicloud import PyiCloudService
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


class MyCalendar:
    def __init__(self):
        # Читаем логин и пароль из переменных окружения
        username = os.getenv("ICLOUD_USERNAME")
        password = os.getenv("ICLOUD_PASSWORD")

        if not username or not password:
            raise ValueError("Логин или пароль для iCloud не найдены. Убедитесь, что они указаны в .env файле.")

        # Инициализируем подключение к iCloud
        self.api = PyiCloudService(username, password)

    def check_availability(self, date, time):
        """
        Проверяет, занято ли указанное время в календаре.
        """
        date_time_str = f"{date} {time}"
        date_time_obj = datetime.strptime(date_time_str, "%d.%m %H:%M")
        events = self.api.calendar.events.get(date_time_obj.date(), date_time_obj.date())

        for event in events:
            if event.start == date_time_obj:
                return False  # Время занято
        return True  # Время свободно

    def book_appointment(self, name, surname, service, day, time, phone):
        """
        Записывает клиента на выбранное время в календарь.
        """
        if self.check_availability(day, time):
            date_time_str = f"{day} {time}"
            date_time_obj = datetime.strptime(date_time_str, "%d.%m %H:%M")

            self.api.calendar.create(
                event_title=f"Запись: {service} для {name} {surname}",
                starts=date_time_obj,
                ends=date_time_obj,
                location="Студия Xeni_brows",
                notes=f"Контактный телефон: {phone}"
            )
            return True
        else:
            return False
