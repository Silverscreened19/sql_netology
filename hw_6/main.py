import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import create_tables, Publisher, Book, Shop, Stock, Sale

conn_driver = ''
login = ''
passw = ''
server_name = ''
port = ''
db_name = ''


def insert_data():
    with open('tests_data.json') as f:
        data = json.load(f)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def pub_id_list():
    publ_ids = []
    q = session.query(Publisher.id).all()
    for i in q:
        publ_ids.append(*i)
    return publ_ids


def pub_name_list():
    publ_names = []
    q = session.query(Publisher.name).all()
    for i in q:
        publ_names.append(*i)
    return publ_names


def pub_info_num():
    publ_num = input('Введите идентификатор издателя (publisher): ')
    if int(publ_num) in pub_id_list():
        query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Publisher).join(
            Book).join(Stock).join(Shop).join(Sale).where(Publisher.id == int(publ_num)).all()
        for i in query:
            date = datetime.strptime(
                str(i.date_sale), '%Y-%m-%d').strftime('%d-%m-%Y')
            print(f'{i.title} | {i.name} | {i.price} | {date}')
    else:
        print('id не найден')
        pub_info_name()


def pub_info_name():
    publ_name = input('Введите имя (publisher): ')
    if publ_name in pub_name_list():
        query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Publisher).join(
            Book).join(Stock).join(Shop).join(Sale).where(Publisher.name == publ_name).all()
        for i in query:
            date = datetime.strptime(
                str(i.date_sale), '%Y-%m-%d').strftime('%d-%m-%Y')
            print(f'{i.title} | {i.name} | {i.price} | {date}')
    else:
        print('имя не найдено')


if __name__ == '__main__':
    DSN = f'{conn_driver}://{login}:{passw}:@{server_name}:{port}/{db_name}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    insert_data()
    pub_info_num()
    session.close()
