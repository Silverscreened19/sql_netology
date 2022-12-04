import psycopg2
from pprint import pprint


class Database:

    def __init__(self, cur):
        pass

    def createdb(self):
        '''This method creates a carcass of db.
        '''
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
        print(f'DB created')


class Client:

    def __init__(self, cur):
        pass

    def insert_data(self, name, last_name):
        '''This method creates a new client.

        Input Arguments must be str.
        '''
        cur.execute('''
        INSERT INTO clients_info(name, last_name)
        VALUES(%s, %s)
        RETURNING client_id;
        ''', (name, last_name))
        conn.commit()
        print(
            f'Клиент {name} {last_name} добавлен с номером {cur.fetchone()[0]}')

    def insert_mult_data(self, quantity):
        '''This method creates multiple clients at once.

        Input Arguments must be str.
        '''
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

    def find_full_name(self, client_id):
        '''This method shows full_name of an existing client in db.

        Input Arguments: client_id must be int.
        '''
        cur.execute('''
        SELECT name, last_name FROM clients_info WHERE client_id=%s;
        ''', (client_id, ))
        return cur.fetchall()[0]

    def find_from_name(self, name):
        '''This method shows last name, emails, phone numbers of an existing client in db by its name.

        Input Arguments: name must be str.
        '''
        cur.execute('''
        SELECT last_name, email, p.phone_number FROM clients_info c
        FULL JOIN emails e on c.client_id = e.client_id
        FULL JOIN phone_numbers p on c.client_id = p.client_id
        WHERE name=%s;
        ''', (name,))
        print(cur.fetchall())

    def find_from_l_name(self, last_name):
        '''This method shows name, emails, phone numbers of an existing client in db by its last name.

        Input Arguments: last_name must be str.
        '''
        cur.execute('''
        SELECT name, email, p.phone_number FROM clients_info c
        FULL JOIN emails e on c.client_id = e.client_id
        FULL JOIN phone_numbers p on c.client_id = p.client_id
        WHERE last_name=%s;
        ''', (last_name,))
        print(cur.fetchall())

    def ch_n(self, client_id, new_name):
        '''This method changes client's name by its id.

        Input Arguments: client_id must be int, new_name must be str.
        '''
        if new_name == self.find_full_name(client_id)[0]:
            print(f'Имена совпадают')
        else:
            cur.execute('''
            UPDATE clients_info SET name=%s WHERE client_id=%s;
            ''', (new_name, client_id))
            cur.execute('''
            SELECT * FROM clients_info WHERE client_id=%s;
            ''', (client_id, ))
            conn.commit()
            print(cur.fetchone())

    def ch_ln(self, client_id, new_lst_name):
        '''This method changes client's last name by its id.

        Input Arguments: client_id must be int, new_lst_name must be str.
        '''
        if new_lst_name == self.find_full_name(client_id)[1]:
            print(f'Фамилии совпадают')
        else:
            cur.execute('''
            UPDATE clients_info SET last_name=%s WHERE client_id=%s;
            ''', (new_lst_name, client_id))
            cur.execute('''
            SELECT * FROM clients_info WHERE client_id=%s;
            ''', (client_id,))
            conn.commit()
            print(cur.fetchone())

    def rm_cl(self, client_id):
        '''This method removes client's info from db and shows remaining clients.

        Input Arguments: client_id must be int.
        '''
        cur.execute('''
        DELETE FROM phone_numbers WHERE client_id=%s;
        ''', (client_id,))
        cur.execute('''
        DELETE FROM emails WHERE client_id=%s;
        ''', (client_id,))
        cur.execute('''
        DELETE FROM clients_info WHERE client_id=%s;
        ''', (client_id, ))
        cur.execute('''
        SELECT * FROM clients_info;
        ''')
        conn.commit()
        print(f'Клиент под номером {client_id} удален')
        print(f'Оставшиеся клиенты {cur.fetchall()}')

    def show_info(self):
        '''This method shows all existing clients' info.
        '''
        cur.execute('''
        SELECT * FROM clients_info c
        LEFT JOIN emails e on c.client_id = e.client_id
        LEFT JOIN phone_numbers p on c.client_id = p.client_id;
        ''')
        pprint(cur.fetchall())


class Phone:

    def __init__(self, cur):
        pass

    def add_phone(self, client_id, ph_num):
        '''This method adds a phone number to an existing client in db.

        Input Arguments: client_id must be int, ph_num must be str.
        '''
        cur.execute('''
        INSERT INTO phone_numbers(client_id, phone_number)
        VALUES(%s, %s)
        RETURNING phone_number;
        ''', (client_id, ph_num))
        conn.commit()
        print(f'Номер телефона {cur.fetchone()[0]} добавлен в базу')

    def find_from_phone(self, phone):
        '''This method shows name, last_name, emails of an existing client in db by its phone.

        Input Arguments: phone must be str.
        '''
        cur.execute('''
        SELECT name, last_name, email FROM clients_info c
        LEFT JOIN phone_numbers p on c.client_id = p.client_id
        LEFT JOIN emails e on c.client_id = e.client_id
        WHERE phone_number=%s;
        ''', (phone,))
        print(cur.fetchall())

    def rm_phone(self, client_id):
        '''This method removes client's phone number by its id.

        Input Arguments: client_id must be int
        '''
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


class Email:

    def __init__(self, cur):
        pass

    def add_em(self, client_id, e_mail):
        '''This method adds an email to an existing client in db.

        Input Arguments: client_id must be int, e_mail must be str.
        '''
        cur.execute('''
        INSERT INTO emails(client_id, email)
        VALUES(%s, %s)
        RETURNING email;
        ''', (client_id, e_mail))
        conn.commit()
        print(f'Адрес электронной почты {cur.fetchone()[0]} добавлен в базу')

    def find_from_email(self, email):
        '''This method shows name, last_name, phone numbers of an existing client in db by its email.

        Input Arguments: email must be str.
        '''
        cur.execute('''
        SELECT name, last_name, p.phone_number FROM clients_info c
        LEFT JOIN emails e on c.client_id = e.client_id
        LEFT JOIN phone_numbers p on c.client_id = p.client_id
        WHERE email=%s;
        ''', (email,))
        print(cur.fetchall())

    def rm_e(self, client_id):
        '''This method removes client's email by its id.

        Input Arguments: client_id must be int
        '''
        cur.execute('''
        SELECT client_id, COUNT(email) FROM emails
        GROUP BY client_id;
        ''')
        cur.execute('''
        SELECT COUNT(email) FROM emails WHERE client_id=%s;
        ''', (client_id,))
        email_q = cur.fetchone()
        if email_q[0] == 0:
            print(
                f'У клиента {client_id} отсутствует адрес электронной почты.')
        elif email_q[0] == 1:
            cur.execute('''
            SELECT email FROM emails WHERE client_id=%s;
            ''', (client_id,))
            email = cur.fetchone()[0]
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


if __name__ == '__main__':
    with psycopg2.connect(database='netology_db', user='postgres') as conn:
        with conn.cursor() as cur:
            db = Database(cur)
            client = Client(cur)
            phone = Phone(cur)
            email = Email(cur)
            client.insert_data('Pam', 'Beasley')
            client.insert_mult_data(3)
            print(client.find_full_name(8))
            client.find_from_name('Jack')
            client.find_from_l_name('Smith')
            client.ch_n(8, 'Nina')
            client.ch_ln(8, 'Hagen')
            client.rm_cl(2)
            client.show_info()

            phone.add_phone(2, '+79999999951')
            phone.find_from_phone('+75555555543')
            phone.rm_phone(12)

            email.add_em(2, 'sdfwgw334@gov.com')
            email.find_from_email('nsjldn@gmail.com')
            email.rm_e(2)
    conn.close()
