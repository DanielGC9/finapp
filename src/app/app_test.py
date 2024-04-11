"""
    This module contains the main logic for the app
    using Streamlit.

    Created by: @DanielGuzman and @JuliethAlvarado
    Date: 2023-06-08
    Version: 1.0.0
"""

import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.mandatory_date_range import date_range_picker
from datetime import datetime
from streamlit_option_menu import option_menu
sys.path.append('.')
from src.utils.functions import import_data, pie
from dotenv import load_dotenv
from src.app.data_entry import data_entry
from src.app.home import home

load_dotenv()


def main():
    # DATA
    # import the data to a dataframe
    data = import_data().dropna()
    data['Date'] = data['Date'].astype('datetime64[ns]')
    income = data[data['Category'] == 'Income']
    expenses = data[data['Category'] != 'Income']
    expenses['Month'] = expenses['Date'].dt.strftime('%b')

    today = datetime.now()

    # PAGE

    with st.sidebar:
        selected = option_menu(None, ["Home", "Data Entry"],
                               icons=['house', "list-task"],
                               menu_icon="cast", default_index=0, orientation="vertical",
                               styles={
                                   "container": {"padding": "sidebar", "background-color": "#fafafa"},
                                   "icon": {"color": "black", "font-size": "15px"},
                                   "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "##1f66bd"},
                                   "nav-link-selected": {"background-color": "#1f66bd"},
                                   })
    if selected == 'Home':
        home(expenses, income)
    elif selected == 'Data Entry':
        data_entry(expenses)

    st.sidebar.markdown("""
                        <style>
                        .footer {
                        position: absolute;
                        bottom: 10px;
                        left: 0;
                        width: 100%;
                        text-align: center;
                        font-size: smaller;
                        }
                        </style>
                        """, unsafe_allow_html=True)
    st.sidebar.write('<p style="font-size: smaller;">Made with ❤️ by <br> @DanielGuzman and @JuliethAlvarado </small>', unsafe_allow_html=True)

main()
