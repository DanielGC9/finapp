
import pandas as pd


def new_user(conn, username, password, email, name, lastName):
    query = f'''INSERT INTO users (username, password, email, name, lastName)
                VALUES ('{username}', '{password}', '{email}', '{name}', '{lastName}');'''

    conn.execute(query)
    conn.commit()
    conn.sync()


#new_user('danalv', '098765', 'dan@finapp.com', 'Dann', 'Alvarado')

def users_data(conn):
    query = '''SELECT username, password, email, name 
                FROM users'''
    table1 = conn.execute(query)
    table = table1.fetchall()
    columns = [description[0] for description in table1.description]
    df = pd.DataFrame(table, columns=columns)
    users_list = df['username'].tolist()
    password_list = df['password'].tolist()
    emails_list = df['email'].tolist()
    names_list = df['name'].tolist()
    return users_list, password_list, emails_list, names_list
