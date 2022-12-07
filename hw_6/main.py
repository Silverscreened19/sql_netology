import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables

# создаем движок-абстракцию для подключения  бд:
DSN = 'postgresql://postgres:qweASD!:@localhost:5432/hw_6'  # строка подключения к постгрес
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()
