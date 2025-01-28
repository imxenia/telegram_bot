from sqlalchemy import Column, Integer, String
from db_config import Base, Session

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)  # уникальный user_id
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    service = Column(String, nullable=True)
    added_service = Column(String, nullable=True)
    day = Column(String, nullable=True)
    time = Column(String, nullable=True)
    phone = Column(String, nullable=True)

def save_client_data(user_id, name=None, surname=None, service=None, added_service=None, day=None, time=None, phone=None):
    """Добавляет или обновляет данные клиента в базе."""
    session = Session()
    try:
        # Проверяем, существует ли клиент с указанным user_id
        client = session.query(Client).filter_by(user_id=user_id).first()

        if client:
            # Если клиент существует, обновляем только новые данные
            if service:
                client.service = service
            if added_service:
                client.added_service = added_service
            if day:
                client.day = day
            if time:
                client.time = time
            if name or surname or phone:
                print(f"Имя, фамилия и телефон не обновлены для существующего клиента user_id {user_id}.")
            print(f"Данные клиента с user_id {user_id} обновлены.")
        else:
            # Если клиента нет, создаём нового
            if not (name and surname and phone):
                print(f"Ошибка: Для нового клиента user_id {user_id} необходимо указать имя, фамилию и телефон.")
                return
            client = Client(
                user_id=user_id,
                name=name,
                surname=surname,
                service=service,
                added_service=added_service,
                day=day,
                time=time,
                phone=phone
            )
            session.add(client)
            print(f"Новый клиент {name} {surname} (user_id: {user_id}) добавлен.")

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка при сохранении данных клиента: {e}")
    finally:
        session.close()