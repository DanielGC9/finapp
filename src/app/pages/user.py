import sys
import time
import streamlit as st
from datetime import datetime
sys.path.append('.')
from src.utils.conn_DB import DB

db = DB()

def user_page(name, userId):
    st.header("Configuration")

    categories, i = db.categories_user(userId)
    
    if categories == []: 
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
        
        cat = st.text_input(label='Ingresa tus categorías separadas por coma',value=i.replace(",", ', '),
                            placeholder='comida, trasnporte')
        cat = cat.replace(" ", "")
        st.write(f"Categorías:{cat}")

        if st.button("Actualizar categorías"):
            with st.spinner('Wait for it...'):
                time.sleep(1)
            #db.update_categories(userId, cat, datetime.now())
            st.toast("Categorías actualizadas", icon="🚀")
            time.sleep(3)
            st.rerun()




