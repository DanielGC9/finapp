"""
    This module contains the main logic for the app
    using Streamlit.

    Created by: @DanielGuzman
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
from src.app.tabs import summary_page, categories_page

load_dotenv()
st.set_page_config(page_title="FinApp", page_icon="💳", layout="wide")

today = datetime.now()

def main():
    # import the data to a dataframe
    data = import_data().dropna()
    data['Date'] = data['Date'].astype('datetime64[ns]')
    income = data[data['Category'] == 'Income']
    expenses = data[data['Category'] != 'Income']
    expenses['Month'] = expenses['Date'].dt.strftime('%b')

    # Page settings
    st.write("# Expense Management",)

    # Tabs navigation
    tab1, tab2, tab3 = st.tabs(['Sumary', 'By Category', 'Debts'])

    with tab1:
        summary_page(expenses, income)
    with tab2:
        categories_page(expenses, income)

    st.sidebar.image("data/images/finapp.png",caption="Personal Finance Dashboard")

    with st.sidebar:
        selected = option_menu(None, ["Summary", "Categories"],
        icons=['house', "list-task"],
        menu_icon="cast", default_index=0, orientation="vertical",
        styles={
            "container": {"padding": "sidebar", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "15px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "##1f66bd"},
            "nav-link-selected": {"background-color": "#1f66bd"},
        }
        )
    if selected == "Summary":
        summary_page(expenses, income)
    elif selected == "Categories":
        categories_page(expenses, income)

    st.sidebar.write('<p>Made with ❤️ by <br> @DanielGuzman <br> @JuliethAlvarado </p>', unsafe_allow_html=True, )
