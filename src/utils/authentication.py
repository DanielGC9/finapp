import streamlit as st
import pandas as pd
from gsheetsDB import GoogleSheets
from functions import validate_email, validate_username
from datetime import datetime
import bcrypt

GSheets = GoogleSheets('users')

emails = GSheets.query_data('''SELECT email 
                            FROM users 
                            WHERE email IS NOT NULL''')['email'].tolist()

users = GSheets.query_data('''SELECT username 
                            FROM users 
                            WHERE username IS NOT NULL''')['username'].tolist()

def hash_password(password):
   password = "MySecretPassword" 
   password_bytes = password.encode('utf-8')
   hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
   return hashed_bytes.decode('utf-8')

today = datetime.now()
user_id = 1
createdAt = today.strftime('%Y-%m-%d %H:%M:%S')
updatedAt = today.strftime('%Y-%m-%d %H:%M:%S')

def sign_in():
    with st.form(key='Sing Up', clear_on_submit=False):
        st.subheader(':green[Sign Up] :wink:')
        name = st.text_input(':blue[Name] :sunglasses:', placeholder='Enter your name',)
        lastName = st.text_input(':blue[Last Name] :sunglasses:', placeholder='Enter your last name')
        username = st.text_input(':blue[Username] :sunglasses:', placeholder='Enter your username')
        mail = st.text_input(':blue[Email] :sunglasses:', placeholder='Enter your email')
        password1 = st.text_input(':blue[Password] :sunglasses:', type='password', placeholder='Enter your password')
        password2 = st.text_input(':blue[Confirm Password] :sunglasses:',  type='password', placeholder='Confirm your password')


        if name:
            if len(username) >= 4:
                if validate_username(username):
                    if username not in users:
                        if validate_email(mail):
                            if mail not in emails:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        password_hash = hash_password(password1)
                                        df = pd.DataFrame({
                                                            'userId': [1],
                                                            'username': [username],
                                                            'password': [password_hash],
                                                            'email': [mail],
                                                            'name': [name],
                                                            'lastName': [lastName],
                                                            'createdAt': [createdAt],
                                                            'updatedAt': [updatedAt],
                                                            'deletedAt': [pd.NaT]
                                                            })
                                        GSheets.new_user(df)
                                        st.success('You have successfully signed up!')
                                    else: st.warning('Passwords do not match')
                                else: st.warning('Password too short')
                            else: st.warning('The email is already exist')
                        else: st.warning('The email is not valid')
                    else: st.warning('The username is already exist')
                else: st.warning('Username is not valid')
            else: st.warning('Username too short')

        st.form_submit_button(label='Sign Up')

sign_in()

# Tutorial
# https://www.youtube.com/watch?v=8X1OidYYVQw