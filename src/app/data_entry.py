import streamlit as st
from datetime import datetime
from src.utils.conn_DB import * # La función para ingresar data a la tabla


def data_entry(input_df):
    st.write("# :dollar: Data Entry")

    with st.form('data-entry'):
        category = st.selectbox('Categoría',
                                input_df['Category'].unique(),
                                index=None,
                                placeholder='Food')
        date = st.date_input(label='Fecha',
                             value=datetime.now().date(),
                             key='date')
        description = st.text_input(label='Concepto',
                                    max_chars=30,
                                    placeholder='Mercado',
                                    help='Ingresa una breve descripción de tu gasto, ingreso o deuda. (max 30 char)')
        amount = st.number_input(label='Cantidad',
                                 min_value=0,
                                 value=None,
                                 placeholder='$100.000',
                                 format='%d',
                                 help='Ingresa el monto de tu gasto, ingreso o deuda, sin signos, puntos ni comas.')
        payment_method = st.selectbox('Método de pago',
                                      input_df['PayMethod'].unique(),
                                      index=None,
                                      placeholder='Efectivo')
        current_month = st.checkbox(label='Este gasto corresponde a este mes',
                                    value=True)
        submit = st.form_submit_button('Agregar')

    if submit:
        st.write(category, date, description, amount, payment_method, current_month)
        # Se agrega a la tabla :)
