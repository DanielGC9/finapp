
import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection


query_read = '''
SELECT 
    userId,
    username,
    password,
    email,
    name,
    lastName,
    createdAt,
    updatedAt,
    deletedAt

FROM users
WHERE username IS NOT NULL
'''
st.cache_data.clear()

class GoogleSheets():
    def __init__(self,sheet_name):
        self.conn = st.connection("gsheets", type=GSheetsConnection)
        self.sname = sheet_name

    def read_data(self):
        return self.conn.query(query_read, worksheet=self.sname)
    
    def query_data(self, query):
        return self.conn.query(query, worksheet=self.sname)
    

    def update(self, data):
        self.conn.update(worksheet=self.sname, data=data)

    def new_user(self, new):
        current = self.conn.query(query_read, worksheet=self.sname)
        current_userId = self.conn.query('''SELECT max(userId) AS Id 
                                         FROM users''',
                                          worksheet=self.sname)
        new['userId'] = current_userId['Id'] + 1
        final = pd.concat([current, new])
        self.conn.update(worksheet=self.sname, data=final)

