import sys
import time
import streamlit as st
from datetime import datetime
from streamlit_extras.add_vertical_space import add_vertical_space
sys.path.append('.')
from src.utils.conn_DB import DB
from src.utils.functions import list_to_string

db = DB()

def user_page(name, userId):
    default_categories = ['🍛 Alimentación', '🏠 Hogar', '🚙 Transporte',
                            '💰 Ingreso', '🏦 Cuentas', '🎁 Otros',
                            '🍔 Comida rápida', '🛒 Compras', '📚 Educación',
                            '🩺 Salud', '🎟 Entretenimiento', '🔺Extra']
    # Existing categories
    user_categories = db.categories_user(userId)

    if user_categories == ['']:
        st.subheader(f"{name}, empecemos definiendo las categorías para tus gastos 🖋")
        st.markdown("Selecciona las categorías que mejor se ajusten a ti.")

    else:
        st.header("Configuración")
        st.write("Aquí puedes configurar las categorías que más se ajusten a ti.")

    selected_categories = []

    c1, c2 = st.columns([0.7,0.3])
    with c1:
        st.subheader("Categorías disponibles:")
        col1, col2, col3, col4 = st.columns(4)

        i = 0
        for col in [col1, col2, col3, col4]:
            j = 0
            while j < 3:
                cat=default_categories[i]
                key = cat+str(i)
                if cat in user_categories:
                    selected_categories.append(col.toggle(cat, value=True, key=key))
                else:
                    selected_categories.append(col.toggle(cat, value=False, key=key))
                i+=1
                j+=1

        # Custom categories
        add_vertical_space(1)
        st.subheader("Categorías personalizadas:")
        st.markdown("¡También puedes agregar categorías personalizadas! 😎 Escoge un emoji \
                    en el siguiente \
                    [enlace](https://www.webfx.com/tools/emoji-cheat-sheet/), haz click en el ícono \
                    deseado y pégalo en el recuadro. A continuación escribe el nombre de la categoría \
                    que deseas añadir y actualiza las categorías.")

        user_custom_cat = [cat for cat in user_categories if cat not in default_categories]

        custom_cat = []
        col_1, col_2, col_3 = st.columns(3)
        if len(user_custom_cat)==0:
            with col_1:
                custom1 = st.text_input(label='Personalizada 1',
                                        max_chars=20,
                                        placeholder="🐾 Mascota")
            with col_2:
                custom2 = st.text_input(label='Personalizada 2',
                                        max_chars=20,
                                        placeholder="👨‍👩‍👦 Familia")
            with col_3:
                custom3 = st.text_input(label='Personalizada 3',
                                        max_chars=20,
                                        placeholder="🛵 Moto")
            custom_cat = [custom1, custom2, custom3]
        else:
            st.write(" ")

        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #ffffff;
            color:;
        }
        div.stButton > button:hover {
            background-color: #46847e;
            color:#000000;
            }
        </style>""", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            add_vertical_space(1)
            if st.button('Guardar categorías', key='guardar'):
                c1.success("Categorías guardadas 👍")

        with col3:
            add_vertical_space(1)
            if st.button('Actualizar categorías', key='actualizar'):
                c1.warning("Categorías actualizadas 👍")

    # Use a mask to get the categories that the user selected
    mask = [x for x, selected in zip(default_categories, selected_categories) if selected]
    updated_categories = mask + custom_cat
    with c2:
        with st.container(border=True):
            st.subheader('Estas son tus categorías:')
            col5, col6 = st.columns(2)
            k=0
            for cat in updated_categories:
                if k < 8:
                    col5.write(cat)
                    k+=1
                else:
                    col6.write(cat)

    updated_list = list_to_string(default_categories)

    if st.button("Guardar categorías"):
        with st.spinner('Espera un momento...'):
            time.sleep(1)
        db.update_categories(userId, updated_list, datetime.now())
        st.toast("Categorías actualizadas", icon="🚀")
        time.sleep(3)
        st.rerun()


    # st.subheader("Configuración de categorías 🖋")
    # st.markdown("Si quieres añadir emojis a tus categorías, puedes encontrarlos en el siguiente \
    #             [enlace](https://www.webfx.com/tools/emoji-cheat-sheet/)")

    # cat = st.text_input(label='Ingresa tus categorías separadas por coma',value=i,
    #                     placeholder='comida, transporte')
    # cat = cat.replace(" ", "")
    # st.write(f"Categorías:{cat}")

    # if st.button("Actualizar categorías"):
    #     with st.spinner('Wait for it...'):
    #         time.sleep(1)
    #     db.update_categories(userId, cat, datetime.now())
    #     st.toast("Categorías actualizadas", icon="🚀")
    #     time.sleep(3)
    #     st.rerun()
