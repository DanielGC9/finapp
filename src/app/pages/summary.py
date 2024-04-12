""" 
Page that shows the summary of the expenses
"""

import sys
import streamlit as st
sys.path.append('.')
from src.utils.conn_DB import DB
from src.app.tabs import summary_tab, categories_tab
from src.app.pages.expenses import expenses_page

dataBase = DB()


def summary_page(name, userId):
    # import the data to a dataframe
    st.subheader(f"Hola {name}, este es el resumen de tus gastos")
    data = dataBase.expenses_user(userId)#.dropna()
    data['date'] = data['date'].astype('datetime64[ns]')
    income = data[data['category'] == 'Income']
    expenses = data[data['category'] != 'Income']
    expenses['Month'] = expenses['date'].dt.strftime('%b')

    if len(data) == 0:
        st.info(f"uuff, parece que aún no has registrado gastos 😓. Haz click en el botón para empezar")
        if st.button("¡Agrega tus gastos!"):
            expenses_page(name, userId)
    else:
        # Page settings
        st.write("# Expense Management",)

        #st.sidebar.image("data/images/finapp.png",caption="Personal Finance Dashboard")
        # Tabs navigation
        tab1, tab2, tab3 = st.tabs(['Sumary', 'By Category', 'Debts'])

        with tab1:
            summary_tab(expenses, income)
        with tab2:
            categories_tab(expenses, income)
