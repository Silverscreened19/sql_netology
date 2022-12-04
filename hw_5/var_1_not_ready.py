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
        email VARCHAR(50) UNIQUE
        );
    CREATE TABLE IF NOT EXISTS phone_numbers(
        phone_id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients_info(client_id),
        phone_number VARCHAR(12) UNIQUE
        );
        ''')
    conn.commit()
    print(f'done')

def insert_data(cur):
    name = input('Введите имя клиента: ')
    last_name = input('Введите фамилию клиента: ')
    cur.execute('''
    INSERT INTO clients_info(name, last_name)
    VALUES(%s, %s)
    RETURNING client_id;
    ''', (name, last_name))
    print(f'Клиент {name} {last_name} добавлен с номером {cur.fetchone()[0]}')

def insert_mult_data(cur):
    quantity = int(input('Введите количество клиентов: '))
    clients_list = []
    while len(clients_list) < quantity:
        name = input('Введите имя клиента: ')
        last_name = input('Введите фамилию клиента: ')
        clients_list.append((name, last_name), )
    cur.executemany('''
    INSERT INTO clients_info (name, last_name)
    VALUES(%s, %s)''', (clients_list))
    conn.commit()
    print(f'{quantity} клиента(-ов) внесено в базу')

def add_phone(cur):
    client_id = input('Введите номер клиента: ')
    ph_num = input('Введите номер телефона: ')
    cur.execute('''
    INSERT INTO phone_numbers(client_id, phone_number)
    VALUES(%s, %s)
    RETURNING phone_number;
    ''', (client_id, ph_num))
    conn.commit()
    print(f'Номер телефона {cur.fetchone()[0]} добавлен в базу')

def add_em(cur):
    client_id = input('Введите номер клиента: ')
    e_mail = input('Введите электронную почту: ')
    cur.execute('''
    INSERT INTO emails(client_id, email)
    VALUES(%s, %s)
    RETURNING email;
    ''', (client_id, e_mail))
    conn.commit()
    print(f'Адрес электронной почты {cur.fetchone()[0]} добавлен в базу')

def find_full_name(cur):
    cur.execute('''
    SELECT name, last_name FROM clients_info WHERE client_id=%s;
    ''', (client_id))
    return cur.fetchall()[0]

def find_from_name(cur):
    cur.execute('''
    SELECT last_name, email, p.phone_number FROM clients_info c
    LEFT JOIN emails e on c.client_id = e.client_id
    LEFT JOIN phone_numbers p on e.client_id = p.client_id
    WHERE name=%s;
    ''', (name,))
    print(cur.fetchall())

def find_from_l_name(cur):
    cur.execute('''
    SELECT name, email, p.phone_number FROM clients_info c
    LEFT JOIN emails e on c.client_id = e.client_id
    LEFT JOIN phone_numbers p on e.client_id = p.client_id
    WHERE last_name=%s;
    ''', (last_name,))
    print(cur.fetchall())

def find_from_email(cur):
    cur.execute('''
    SELECT name, last_name, p.phone_number FROM clients_info c
    LEFT JOIN emails e on c.client_id = e.client_id
    LEFT JOIN phone_numbers p on e.client_id = p.client_id
    WHERE email=%s;
    ''', (email,))
    print(cur.fetchall())

def find_from_phone(cur):
    cur.execute('''
    SELECT name, last_name, email FROM clients_info c
    LEFT JOIN emails e on c.client_id = e.client_id
    LEFT JOIN phone_numbers p on e.client_id = p.client_id
    WHERE phone_number=%s;
    ''', (phone,))
    print(cur.fetchall())

def ch_n(cur):
    new_name = input('Введите новое имя: ')
    if new_name == find_full_name(cur)[0]:
        print(f'Имена совпадают')
    else:
        cur.execute('''
        UPDATE clients_info SET name=%s WHERE client_id=%s;
        ''', (new_name, client_id))
        cur.execute('''
        SELECT * FROM clients_info WHERE client_id=%s;
        ''', (client_id))
        conn.commit()
        print(cur.fetchone())

def ch_ln(cur):
    new_lst_name = input('Введите новую фамилию: ')
    if new_lst_name == find_full_name(cur):
        print(f'Фамилии совпадают')
    else:
        cur.execute('''
        UPDATE clients_info SET last_name=%s WHERE client_id=%s;
        ''', (new_lst_name, client_id))
        cur.execute('''
        SELECT * FROM clients_info WHERE client_id=%s;
        ''', (client_id))
        conn.commit()
        print(cur.fetchone())

def rm_e(cur):
    cur.execute('''
    SELECT client_id, COUNT(email) FROM emails
    GROUP BY client_id;
    ''')
    cur.execute('''
    SELECT COUNT(email) FROM emails WHERE client_id=%s;
    ''', (client_id,))
    email_q = cur.fetchone()
    if email_q[0] == 0:
        print(f'У клиента {client_id} отсутствует адрес электронной почты.')
    elif email_q[0] == 1:
        cur.execute('''
        SELECT email FROM emails WHERE client_id=%s;
        ''', (client_id,))
        email = cur.fetchone()[0]
        print(f'Электронная почта {email} будет удалена')
        cur.execute('''
        DELETE FROM emails WHERE client_id=%s;
        ''', (client_id,))
        cur.execute('''
        SELECT * FROM emails;
        ''')
        conn.commit()
        print(f'Электронная почта {email} удалена')
    else:
        cur.execute('''
        SELECT email_id, email FROM emails WHERE client_id=%s;
        ''', (client_id,))
        email = cur.fetchall()
        print(f'Выберите номер адреса для удаления: {email}')
        email_num = int(input())
        cur.execute('''
        DELETE FROM emails WHERE email_id=%s;
        ''', (email_num,))
        cur.execute('''
        SELECT email FROM emails WHERE client_id=%s;
        ''', (client_id,))
        conn.commit()
        print(f'Электронная почта удалена')

def rm_phone(cur):
    cur.execute('''
    SELECT client_id, COUNT(phone_number) FROM phone_numbers
    GROUP BY client_id;
    ''')
    cur.execute('''
    SELECT COUNT(phone_number) FROM phone_numbers WHERE client_id=%s;
    ''', (client_id,))
    num_q = cur.fetchone()
    if num_q[0] == 0:
        print(f'У клиента {client_id} отсутствует номер телефона')
    elif num_q[0] == 1:
        cur.execute('''
        SELECT phone_number FROM phone_numbers WHERE client_id=%s;
        ''', (client_id,))
        number_ = cur.fetchone()[0]
        print(f'Телефонный номер {number_} будет удален')
        cur.execute('''
        DELETE FROM phone_numbers WHERE client_id=%s;
        ''', (client_id,))
        cur.execute('''
        SELECT * FROM phone_numbers;
        ''')
        conn.commit()
        print(f'Телефонный номер {number_} удален')
    else:
        cur.execute('''
        SELECT phone_id, phone_number FROM phone_numbers WHERE client_id=%s;
        ''', (client_id,))
        number_ = cur.fetchall()
        print(f'Выберите номер телефона для удаления: {number_}')
        ph_num = int(input())
        cur.execute('''
        DELETE FROM phone_numbers WHERE phone_id=%s;
        ''', (ph_num,))
        cur.execute('''
        SELECT phone_id, phone_number FROM phone_numbers WHERE client_id=%s;
        ''', (client_id,))
        conn.commit()
        print(cur.fetchall())

def rm_cl(cur):
    cur.execute('''
    DELETE FROM clients_info WHERE client_id=%s;
    ''', (client_id, ))
    cur.execute('''
    SELECT * FROM clients_info;
    ''')
    conn.commit()
    print(cur.fetchall())

def show_info(cur):
    cur.execute('''
    SELECT * FROM clients_info c
    LEFT JOIN emails e on c.client_id = e.client_id
    LEFT JOIN phone_numbers p on e.client_id = p.client_id;
    ''')
    pprint(cur.fetchall())

def help():
    help_ = (f'Введите команду:\nclear - очистить бд,'
            f'\nclient - добавить нового клиента,'
            f'\nmult_client - добавить несколько клиентов,'
            f'\nadd_ph - добавить телефон для существующего клиента,'
            f'\nadd_e - добавить электронную почту для существующего клиента,'
            f'\nch_n - изменить имя клиента,'
            f'\nch_ln - изменить фамилию клиента,'
            f'\nrm_e - удалить электронную почту клиента,'
            f'\nrm_ph - удалить телефон для существующего клиента,'
            f'\nrm_cl - удалить существующего клиента,'
            f'\nfind -  найти клиента по его имени,'
            f'\nfind_ln - найти клиента по его фамилии,'
            f'\nfind_em - найти клиента по его электронной почте,'
            f'\nfind_ph - найти клиента по его номеру телефона,'
            f'\nshow_info - вывести полную информацию о клиентах в бд')
    return help_

if __name__ == '__main__':
    print(help())
    with psycopg2.connect(database='netology_db', user='postgres') as conn:
        with conn.cursor() as cur:
            while True:
                command = input().lower()
                if command == 'clear':
                    createdb(cur)
                    conn.close()
                if command == 'client':
                    insert_data(cur)
                if command == 'mult_client':
                    insert_mult_data(cur)
                if command == 'add_ph':
                    add_phone(cur)
                if command == 'add_e':
                    add_em(cur)
                if command == 'ch_n':
                    client_id = input('Введите номер клиента: ')
                    ch_n(cur)
                if command == 'ch_ln':
                    client_id = input('Введите номер клиента: ')
                    ch_ln(cur)
                if command == 'rm_e':
                    client_id = input('Введите номер клиента: ')
                    rm_e(cur)
                if command == 'rm_ph':
                    client_id = input('Введите номер клиента: ')
                    rm_phone(cur)
                if command == 'rm_cl':
                    client_id = input('Введите номер клиента: ')
                    rm_cl(cur)
                if command == 'find':
                    name = input('Введите имя клиента: ')
                    find_from_name(cur)
                if command == 'find_ln':
                    last_name = input('Введите фамилию клиента: ')
                    find_from_l_name(cur)
                if command == 'find_em':
                    email = input('Введите электронную почту: ')
                    find_from_email(cur)
                if command == 'find_ph':
                    phone = input('Введите номер телефона: ')
                    find_from_phone(cur)
                if command == 'show_info':
                    show_info(cur)
        conn.close()
