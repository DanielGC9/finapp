"""
    This module contains the main logic for the app
    using Streamlit.

    Created by: @DanielGuzman
    Date: 2023-06-08
    Version: 1.0.0
"""

import sys
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime
#from streamlit_options_menu import option_menu
sys.path.append('.')
from src.utils.functions import import_data

today = datetime.now()
# import the data to a dataframe
data = import_data().dropna()
income = data[data['Category'] == 'Income']
expences = data[data['Category'] != 'Income']

st.set_page_config(page_title="Notion Dashboard", page_icon="💳", layout="wide")

#def summary_page():
    

st.subheader("📊 Personal Finance Dashboard")

st.sidebar.image("data/images/finapp.png",caption="Personal Finance Dashboard")

st.sidebar.header('Filters')
category = st.sidebar.multiselect(
    'Select Category',
    options=expences['Category'].unique(),
    default=expences['Category'].unique()
)

pay_method = st.sidebar.multiselect(
    'Select Pay Method',
    options=expences['PayMethod'].unique(),
    default=expences['PayMethod'].unique()
)

start_date = st.sidebar.date_input(
    'Start Date',
    value=datetime.now().replace(day=1).date(),
)

end_date = st.sidebar.date_input(
    'End Date',
    value=datetime.now().date()
)

# category = st.sidebar.selectbox(
#     'Select Category',
#     options=expences['Category'].unique(),
# )
income_f = income.query('Date <= @end_date')

expences_f = expences.query(
    'Category == @category & PayMethod == @pay_method & Date >= @start_date & Date <= @end_date'
)

def metrics():
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Records', expences_f.shape[0], delta= f'{category[0]} expenses')    
    col2.metric("Total Amount", value=f"{expences_f['Amount'].sum():,.0f}$")
    col3.metric("Percentage", value=f"{expences_f['Amount'].sum() / income_f['Amount'].sum() * 100:.2f}%")
    col4.metric("Income", value=f"{income_f['Amount'].sum():,.0f}$")

    style_metric_cards(background_color='white', border_left_color='#1f66bd')

metrics()

st.dataframe(expences_f)
st.dataframe(income_f)