import sys
import time
import streamlit as st
from datetime import datetime
from streamlit_extras.add_vertical_space import add_vertical_space
sys.path.append('.')
from src.utils.conn_DB import DB

db = DB()

def user_page(name, userId):
    st.header("Configuration")

    default_categories = ['🍛 Alimentación', '🏠 Hogar', '🚙 Transporte', 
                          '💰 Ingreso', '🏦 Cuentas', '🎁 Otros', 
                          '🍔 Comida rápida', '🛒 Compras', '📚 Educación', 
                          '🩺 Salud', '🎟 Entretenimiento', '🔺Extra']
    user_categories = []

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
                user_categories.append(col.toggle(cat, value=True, key=key))
                i+=1
                j+=1

    #use a mask to get the categories that the user selected
    mask = [x for x, selected in zip(default_categories, user_categories) if selected]
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
            c1.success("Categorías guardadas '👍'")
        
    with col3:
        add_vertical_space(2)
        if st.button('Actualizar categorías'):
            c1.warning("Categorías actualizadas '👍'")




        # for cat in default_categories:
        #     key = cat+str(i)
        #     col.checkbox(cat, value=True, key=key)

    categories, i = db.categories_user(userId)
    
    if categories == ['']: 
        st.subheader(f" {name} empecemos definiendo las categorias para tus gastos 🖋")
        st.markdown("Si quieres añadir emojis a tus categorías, puedes encontrarlos en el siguiente \
                    [enlace](https://www.webfx.com/tools/emoji-cheat-sheet/)")
        cat = st.text_input(label='Ingresa tus categorías separadas por coma',
                            placeholder='comida, trasnporte',)

        cat = cat.replace(" ", "")
        lista = cat.split(",")
        st.write(f"Categorías:{lista}")
        if st.button("Guardar categorías"):
            db.add_categories(userId, cat)
            st.success("Categorías guardadas")
            time.sleep(3)
            st.rerun()

    else:
        st.subheader("Configuración de categorías 🖋")
        st.markdown("Si quieres añadir emojis a tus categorías, puedes encontrarlos en el siguiente \
                    [enlace](https://www.webfx.com/tools/emoji-cheat-sheet/)")
        
        cat = st.text_input(label='Ingresa tus categorías separadas por coma',value=i,
                            placeholder='comida, trasnporte')
        cat = cat.replace(" ", "")
        st.write(f"Categorías:{cat}")

        if st.button("Actualizar categorías"):
            with st.spinner('Wait for it...'):
                time.sleep(1)
            db.update_categories(userId, cat, datetime.now())
            st.toast("Categorías actualizadas", icon="🚀")
            time.sleep(3)
            st.rerun()




