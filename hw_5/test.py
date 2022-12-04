import psycopg2
from pprint import pprint

def createdb(cur):
    cur.execute('''
    DROP TABLE phone_numbers;
    DROP TABLE emails;
    DROP TABLE clients_info;
    CREATE TABLE IF NOT EXISTS clients_info(
        client_id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL
        );
    CREATE TABLE IF NOT EXISTS emails(
        email_id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients_info(client_id),
        email VARCHAR(50)
        );
    CREATE TABLE IF NOT EXISTS phone_numbers(
        phone_id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients_info(client_id),
        phone_number INT
        );
        ''')
    conn.commit()
    print(f'Table is created')

def add_info(cur):
    name = input('Введите имя клиента: ')
    last_name = input('Введите фамилию клиента: ')
    cur.execute('''
    INSERT INTO clients_info(name, last_name) VALUES(%s, %s)
    RETURNING client_id;
    ''', (name, last_name))
    print(cur.fetchone())

def find_name(cur):
    id = input('Введите номер клиента: ')
    cur.execute('''
    SELECT name, last_name FROM clients_info WHERE client_id=%s;
    ''', (id))
    return cur.fetchall()[0]

def count_e(cur):
    id = input('Введите номер клиента: ')
    cur.execute('''
    SELECT client_id, COUNT(email) FROM emails
    GROUP BY client_id;
    ''')
    cur.execute('''
    SELECT COUNT(email) FROM emails WHERE client_id=%s;
    ''', (id))
    email_q = cur.fetchone()
    print(email_q[0])

def show_info(cur):
    cur.execute('''
    SELECT * FROM clients_info c
    LEFT JOIN emails e on c.client_id = e.client_id
    LEFT JOIN phone_numbers p on e.client_id = p.client_id;
    ''')
    pprint(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database='netology_db', user='postgres') as conn:
            with conn.cursor() as cur:
                # print(find_name(cur))
                show_info(cur)
#                 count_e(cur)
#                 # new_name = input('Введите новое имя: ')
#                 # # if new_name != find_name(cur):
#                 # #     cur.execute('''
#                 # #     UPDATE clients_info SET name = %s WHERE client_id=%s;
#                 # #     '''), (new_name, id)
#                 # cur.execute('''
#                 #     UPDATE clients_info SET name='Lola' WHERE client_id=1;
#                 #     '''), (new_name, client_id)
    conn.close()



# quantity = int(input('Введите количество клиентов: '))
# clients_list = []
# while len(clients_list) < quantity:
#     name = input('Введите имя клиента: ')
#     last_name = input('Введите фамилию клиента: ')
#     clients_list.append((name, last_name), )
#     print(len(clients_list))
# print(clients_list)

# with psycopg2.connect(database='netology_db', user='postgres') as conn:
#     with conn.cursor() as cur:
#         cur.executemany('''INSERT INTO clients_info (name, last_name)
#         VALUES(%s, %s)''', (clients_list))
#         conn.commit()
        # print(cur.fetchall())
