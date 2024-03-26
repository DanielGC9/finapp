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
from datetime import datetime
from streamlit_option_menu import option_menu
sys.path.append('.')
from src.utils.functions import import_data, pie
#from src.app.pages.summary import summary_page
#from src.app.pages.categories import categories_page

today = datetime.now()
# import the data to a dataframe
data = import_data().dropna()
data['Date'] = data['Date'].astype('datetime64[ns]')
income = data[data['Category'] == 'Income']
expences = data[data['Category'] != 'Income']
expences['Month'] = expences['Date'].dt.strftime('%b')



def summary_page():

    st.write("# Summary",)
    
    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total Records',
                value = expences.shape[0],
                delta= 'All expenses')    
    col2.metric("Total Amount",
                value=f"{expences['Amount'].sum():,.0f}$",
                delta='Total COP amount')
    col3.metric("Percentage", 
                value = f"{expences['Amount'].sum() / income['Amount'].sum() * 100:.2f}%",
                delta = 'Percentage spent')
    col4.metric("Income",
                value=f"{income['Amount'].sum():,.0f}$",
                delta='Total income COP')

    style_metric_cards(background_color='white', border_left_color='#1f66bd')

    st.markdown("""---""")

    div1, div2 = st.columns(2)
    with div1:
        st.header("Expenses")
        def pie(title, dataframe, x, y):
            fig = px.pie(dataframe, values=x, names=y, width=500, height=500)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, theme=None)

        pie('Income',expences, 'Amount', 'Category')
    with div2:
        st.header("Bar Chart")
        def bar(title, dataframe, x, y):
            df = dataframe.groupby(x)[y].sum().reset_index().sort_values(by=y, ascending=False)
            fig = px.bar(df, x=x, y=y, width=500, height=500)
            #fig.update_traces(textposition='inside', textinfo='label')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, theme=None)

        bar('Income',expences, 'Category', 'Amount')

    st.header("Bar Chart")
    def bar(dataframe, x, y):
        df = dataframe.groupby([x, 'Category'])[y].sum().reset_index().sort_values(by=y, ascending=True)
        fig = px.bar(df, x=y, y=x, color='Category', width=500, height=500, orientation='h')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    bar(expences, 'Month', 'Amount')

    st.header("Table")
    st.dataframe(expences, use_container_width=True)

def categories_page():
    st.write("# 💰 Categories")
    st.markdown("""---""")

    st.sidebar.header('Filters')
    category = st.sidebar.multiselect(
        'Select Category',
        options = np.append(['All'], expences['Category'].unique()),
        default=['All']
    )

    if  ['All'] == category:
        category = list(expences['Category'].unique())

    pay_method = st.sidebar.multiselect(
        'Select Pay Method',
        options=np.append(['All'], expences['PayMethod'].unique()),
        default=['All']
    )
    if ['All'] == pay_method:
        pay_method = list(expences['PayMethod'].unique())

    start_date = st.sidebar.date_input(
        'Start Date',
        value=datetime.now().replace(day=1).date(),
    )

    end_date = st.sidebar.date_input(
        'End Date',
        value=datetime.now().date()
    )
    income_f = income.query('Date <= @end_date')

    expences_f = expences.query(
        'Category == @category & PayMethod == @pay_method & Date >= @start_date & Date <= @end_date'
    ).reset_index(drop=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total Records',
                value = expences_f.shape[0],
                delta= 'All expenses')    
    col2.metric("Total Amount",
                value=f"{expences_f['Amount'].sum():,.0f}$",
                delta='Total COP amount')
    col3.metric("Percentage", 
                value = f"{expences_f['Amount'].sum() / income_f['Amount'].sum() * 100:.2f}%",
                delta = 'Percentage spent')
    col4.metric("Income",
                value=f"{income['Amount'].sum():,.0f}$",
                delta='Total income COP')

    style_metric_cards(background_color='white', border_left_color='#1f66bd')


    st.dataframe(expences_f, use_container_width=True)


#st.set_page_config(page_title="Notion Dashboard", page_icon="💳", layout="wide")

st.sidebar.image("data/images/finapp.png",caption="Personal Finance Dashboard")

#summary_page()
#categories_page(income, expences)


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
    summary_page()
elif selected == "Categories":
    categories_page()