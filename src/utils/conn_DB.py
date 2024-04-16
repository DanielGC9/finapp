import sys
import pandas as pd
from datetime import datetime
sys.path.append('.')
from src.utils.connection import conn


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


    def new_expense(self, userId, expense, category, amount, description, paymentMethod, date, thisMonth):
        query = f'''
        INSERT INTO expenses (userId, expense, category, amount, description, paymentMethod, date, thisMonth)
                    VALUES ('{userId}', '{expense}', '{category}', '{amount}', '{description}',
                    '{paymentMethod}', '{date}', '{thisMonth}');
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

    def expenses_all(self):
        query = '''SELECT * FROM expenses'''
        table1 = self.conn.execute(query)
        table = table1.fetchall()
        columns = [description[0] for description in table1.description]
        df = pd.DataFrame(table, columns=columns)
        return df

    def drop_table(self, table):
        query = f'''DROP TABLE {table}'''
        self.conn.execute(query)
        self.conn.commit()
        self.conn.sync()

    def new_table(self):
        query='''
        CREATE TABLE categories(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            userId INTEGER NOT NULL,
            category VARCHAR(500) NOT NULL,
            createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            deletedAt DATETIME DEFAULT NULL,
            FOREIGN KEY (userId) REFERENCES users(id)
        );
        '''
        self.conn.execute(query)
        self.conn.commit()
        self.conn.sync()

    def add_categories(self, userId, category):
        query = f'''
        INSERT INTO categories (userId, category)
                    VALUES ('{userId}', '{category}');
                '''
        self.conn.execute(query)
        self.conn.commit()
        self.conn.sync()

    def update_categories(self, userId, categories, updatedAt):
        query = f'''
        UPDATE categories
        SET category = '{categories}', updatedAt = '{updatedAt}'
        WHERE userId = {userId}
        '''
        self.conn.execute(query)
        self.conn.commit()
        self.conn.sync()

    def categories_user(self, userId):
        query = f'''
            SELECT category
            FROM categories
            WHERE userId = {userId}
        '''
        table1 = self.conn.execute(query)
        if table1.fetchall() == []:
            return [],''
        table = table1.fetchall()
        lista = table[0][0].split(", ")
        return lista

# db = DB()

# db.categories_user(1)
# updated_list = str(["🍛 Alimentación", "🏠 Hogar"])
# print(updated_list)
# db.update_categories(1, updated_list, datetime.now())