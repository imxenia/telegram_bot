from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Абсолютный путь к базе данных
DATABASE_PATH = os.path.abspath('clients_data.db')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# Создание базы и сессии
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
