import os
import pandas as pd
from connection import conn


class DB:
    def __init__(self):
        self.conn = conn

    def new_user(self, username, password, email, name, lastName):
        query = f'''INSERT INTO users (username, password, email, name, lastName)
                    VALUES ('{username}', '{password}', '{email}', '{name}', '{lastName}');'''

        self.conn.execute(query)
        self.conn.commit()
        self.conn.sync()

    def info_user(self, username):
        query = f'''
        SELECT * 
        FROM users 
        WHERE username = '{username}'
        '''
        table1 = self.conn.execute(query)
        info_user = table1.fetchall()[0]
        return info_user


    def users_data(self):
        query = '''SELECT username, password, email, name 
                    FROM users'''
        table1 = self.conn.execute(query)
        table = table1.fetchall()
        columns = [description[0] for description in table1.description]
        df = pd.DataFrame(table, columns=columns)
        users_list = df['username'].tolist()
        password_list = df['password'].tolist()
        emails_list = df['email'].tolist()
        names_list = df['name'].tolist()
        return users_list, password_list, emails_list, names_list


    def new_expense(self, userId, expense, category, amount, description, paymentMethod, date):
        query = f'''
        INSERT INTO expenses (userId, expense, category, amount, description, paymentMethod, date)
                    VALUES ('{userId}', '{expense}', '{category}', '{amount}', '{description}', 
                    '{paymentMethod}', '{date}');
                '''

        self.conn.execute(query)
        self.conn.commit()
        self.conn.sync()


    def expenses_user(self, userId):
        query = f'''SELECT * FROM expenses WHERE userId = {userId}'''
        table1 = self.conn.execute(query)
        table = table1.fetchall()
        columns = [description[0] for description in table1.description]
        df = pd.DataFrame(table, columns=columns)
        return df


# for i, row in data.iterrows():
#     new_expense(conn, 
#                 userId=row['userId'], 
#                 expense=row['Name'], 
#                 category=row['Category'], 
#                 amount=row['Amount'], 
#                 description=row['description'], 
#                 paymentMethod=row['PayMethod'],
#                 date=row['Date'])
