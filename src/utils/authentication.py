import os
import streamlit as st
import pandas as pd
from conn_DB import users_data, new_user
from functions import validate_email, validate_username
from dotenv import load_dotenv
import libsql_experimental as libsql
import bcrypt
import streamlit_authenticator as stauth
import sys
sys.path.append('.')
from src.app.app_test import main


def hash_password(password):
   return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

load_dotenv()

TOKEN = os.environ.get('TOKEN_DB')
URL = os.environ.get('URL_DB')
NAME = os.environ.get('NAME_DB')

conn = libsql.connect(NAME, sync_url=URL, auth_token=TOKEN)
conn.sync()
users, passwords, emails, names = users_data(conn)

#st.set_page_config(page_title="Authentication", page_icon="💳", layout="wide")
# Log in

credentials = {'usernames': {users[i]: {'email': emails[i], 
                                        'failed_login_attempts': 3,
                                        'logged_in': False,
                                        'name': names[i],
                                        'password': passwords[i]} for i in range(len(users))}}

authenticator = stauth.Authenticate(
    credentials, 
    cookie_name='admin', 
    cookie_key='some$ecretkey', 
    cookie_expiry_days=10,
    pre_authorized = 'admin')

with st.container():
    name, authentication_status, username = authenticator.login()

    if not username:
        st.info('Please enter your username and password or sign up')

    if not authentication_status:
        with st.form(key='Sing Up', clear_on_submit=False):
            st.subheader(':green[Sign Up] :wink:')
            name = st.text_input(':blue[Name] :sunglasses:', placeholder='Enter your name',)
            lastName = st.text_input(':blue[Last Name] :sunglasses:', placeholder='Enter your last name')
            username = st.text_input(':blue[Username] :sunglasses:', placeholder='Enter your username', 
                                        help="Must be at least 6 characters long, and you can use '.', '_', and '-'")
            mail = st.text_input(':blue[Email] :sunglasses:', placeholder='Enter your email')
            password1 = st.text_input(':blue[Password] :sunglasses:', type='password', placeholder='Enter your password')
            password2 = st.text_input(':blue[Confirm Password] :sunglasses:',  type='password', placeholder='Confirm your password')


            if name:
                if validate_username(username):
                    if username not in users:
                        if validate_email(mail):
                            if mail not in emails:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        password_hash = hash_password(password1)
                                        new_user(conn, username, password_hash, mail, name, lastName)
                                        st.success('You have successfully signed up!')
                                    else: st.warning('Passwords do not match')
                                else: st.warning('Password too short')
                            else: st.warning('The email is already exist')
                        else: st.warning('The email is not valid')
                    else: st.warning('The username is already exist')
                else: st.warning('Username is not valid')

            st.form_submit_button(label='Sign Up')

    if username in users:
        if authentication_status:
            with st.sidebar:
                st.subheader(f'Welcome {name}')
                authenticator.logout(':green[Logout] :wink:')
            main()

        elif not authentication_status:
            st.error('Username/password is incorrect')

        else:
            st.warning('Please enter your username and password')