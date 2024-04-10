import streamlit as st
from datetime import datetime


def data_entry(input_df):
    st.write("# :dollar: Data Entry")

    with st.form('data-entry'):
        category = st.selectbox('Categoría', input_df['Category'].unique())
        date = st.date_input(label='Fecha', value=datetime.now().date(), key='end_date_cat')
        payment_method = st.selectbox('Método de pago', input_df['PayMethod'].unique())
        st.form_submit_button('Agregar')
