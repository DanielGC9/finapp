import streamlit as st
from src.utils.conn_DB import DB
from src.app.data_entry import data_entry

db = DB()


def expenses_page(name, userId):
    st.header("Expenses")
    st.subheader(f"¡Hola, {name}! :smile:")
    st.subheader("Aquí puedes registrar tus ingresos, gastos o deudas.")

    # import the data to bring categories and payment methods
    data = db.expenses_user(userId)
    data_entry(data, userId)
