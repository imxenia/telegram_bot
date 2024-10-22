import openpyxl

EXCEL_FILE = 'clients_data.xlsx'

def show_notes(bot, message):
    chat_id = message.chat.id

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active

    user_found = False
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[1] == chat_id:
            service = row[4] or 'Услуга не указана'
            added_service = row[5] or ''
            day = row[6] or 'Дата не указана'
            time = row[7] or 'Время не указано'

            if added_service:
                note_message = (f"Вы записаны на услугу «{service}» и «{added_service}» {day} в {time}🌿"
                                f"\nЖдём Вас с нетерпением!")
            else:
                note_message = (f"Вы записаны на услугу «{service}» {day} в {time}🌿"
                                f"\nЖдём Вас с нетерпением!")

            bot.send_message(chat_id, note_message)
            user_found = True
            break

    if not user_found:
        bot.send_message(chat_id, "Записи не найдены.")
