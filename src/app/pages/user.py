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
                    selected_categories.append(col.toggle(cat, value=True, key=key))
                    i+=1
                    j+=1

        # Use a mask to get the categories that the user selected
        mask = [x for x, selected in zip(default_categories, selected_categories) if selected]
        with c2:
            with st.container(border=True):
                st.subheader('Categorías seleccionadas:')
                col5, col6 = st.columns(2)
                k=0
                for cat in mask:
                    if k < 6:
                        col5.write(cat)
                        k+=1
                    else:
                        col6.write(cat)

        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #ffffff;
            color:;
        }
        div.stButton > button:hover {
            background-color: #00ff00;
            color:#ff0000;
            }
        </style>""", unsafe_allow_html=True)
        with col2:
            add_vertical_space(2)
            if st.button('Guardar categorías'):
                c1.success("Categorías guardadas 👍")

        with col3:
            add_vertical_space(2)
            if st.button('Actualizar categorías'):
                c1.warning("Categorías actualizadas 👍")

        updated_list = list_to_string(mask)
        db.update_categories(userId, updated_list, datetime.now())

        st.markdown("Si quieres añadir emojis a tus categorías, puedes encontrarlos en el siguiente \
                    [enlace](https://www.webfx.com/tools/emoji-cheat-sheet/)")
        # cat = st.text_input(label='Ingresa tus categorías separadas por coma',
        #                     placeholder='comida, trasnporte',)

        # cat = cat.replace(" ", "")
        # lista = cat.split(",")
        # st.write(f"Categorías:{lista}")
        # if st.button("Guardar categorías"):
        #     db.add_categories(userId, cat)
        #     st.success("Categorías guardadas")
        #     time.sleep(3)
        #     st.rerun()

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

        #use a mask to get the categories that the user selected
        mask = [x for x, selected in zip(default_categories, selected_categories) if selected]
        with c2:
            with st.container(border=True):
                st.subheader('Estas son tus categorías:')
                col5, col6 = st.columns(2)
                k=0
                for cat in mask:
                    if k < 6:
                        col5.write(cat)
                        k+=1
                    else:
                        col6.write(cat)

        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #ffffff;
            color:;
        }
        div.stButton > button:hover {
            background-color: #00ff00;
            color:#ff0000;
            }
        </style>""", unsafe_allow_html=True)
        with col2:
            add_vertical_space(2)
            if st.button('Guardar categorías'):
                c1.success("Categorías guardadas '👍'")

        with col3:
            add_vertical_space(2)
            if st.button('Actualizar categorías'):
                c1.warning("Categorías actualizadas '👍'")

        st.subheader("Categorías personalizadas:")
        custom_cat = [cat for cat in user_categories if cat not in default_categories]

        col_1, col_2, col_3, col__ = st.columns(4)
        if len(custom_cat)==0:
            with col_1:
                st.text_input(label='Personalizada 1',
                              max_chars=20,
                              placeholder="🐾 Mascota")
            with col_2:
                st.text_input(label='Personalizada 2',
                              max_chars=20,
                              placeholder="👨‍👩‍👦 Familia")
            with col_3:
                st.text_input(label='Personalizada 3',
                              max_chars=20,
                              placeholder="🛵 Moto")
        else:
            st.write(" ")

        st.write(" ")

        updated_list = list_to_string(mask)
        db.update_categories(userId, updated_list, datetime.now())


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
