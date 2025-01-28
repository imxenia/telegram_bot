from db_config import Base, engine
from clients import Client

def initialize_database():
    """Создаёт таблицы в базе данных (если они ещё не созданы)."""
    Base.metadata.create_all(engine)
    print("База данных и таблицы успешно созданы.")
