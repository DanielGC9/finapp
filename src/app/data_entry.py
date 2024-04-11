import streamlit as st
from datetime import datetime
from src.utils.conn_DB import DB

db = DB()


def data_entry(input_df, userId):
    st.write("# :dollar: Data Entry")

    with st.form('data-entry'):
        category = st.selectbox('Categoría',
                                input_df['category'].unique(),
                                index=None,
                                placeholder='Food')
        date = st.date_input(label='Fecha',
                             value=datetime.now().date(),
                             key='date')
        expense = st.text_input(label='Concepto',
                                max_chars=30,
                                placeholder='Mercado',
                                help='Ingresa el concepto de tu gasto, ingreso o deuda. (max 30 char)')
        description = st.text_input(label='Descripción',
                                max_chars=100,
                                placeholder='Mercado en tienda de barrio.',
                                help='Puedes ingresar una breve descripción de tu gasto, ingreso o deuda. (max 100 char)')
        amount = st.number_input(label='Cantidad',
                                 min_value=0,
                                 value=None,
                                 placeholder='$100.000',
                                 format='%d',
                                 help='Ingresa el monto de tu gasto, ingreso o deuda, sin signos, puntos ni comas.')
        payment_method = st.selectbox('Método de pago',
                                      input_df['paymentMethod'].unique(),
                                      index=None,
                                      placeholder='Efectivo')
        current_month = st.checkbox(label='Este gasto corresponde a este mes',
                                    value=True)
        submit = st.form_submit_button('Agregar')

    if submit:
        st.write(category, date, expense, amount, payment_method, current_month)
        db.new_expense(userId, expense, category, amount, description, payment_method, date)
