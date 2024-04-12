"""
    This module contains the main logic for the app
    using Streamlit.

    Created by: @DanielGuzman and @JuliethAlvarado
    Date: 2024-04-11
    Version: 1.0.0
"""

import os
import sys
import streamlit as st
from streamlit_navigation_bar import st_navbar
from streamlit_extras.add_vertical_space import add_vertical_space
sys.path.append('.')
from src.app.pages.expenses import expenses_page
from src.app.pages.summary import summary_page
from src.app.pages.payshare import payshare_page
from src.app.pages.user import user_page


def main(user:list):

    userId = user[0]
    mail = user[3]
    name = user[4]
    lastName = user[5]
    createdAt = user[6]
    updatedAt = user[7]
    #st.set_page_config(initial_sidebar_state="collapsed")

    with st.sidebar:
        st.image("data/images/finapp.png",caption="Finanzas personales",use_column_width=True)
        st.markdown("---")
        st.write(f"{name}, es hora de tomar el control! 💪")
        st.markdown("---")
        add_vertical_space(20)


    parent_dir = os.path.abspath('')
    logo_path = os.path.join(parent_dir, "data/images/bank.svg")
    ima = os.path.join(parent_dir, "data/images/expense.svg") 

    pages = ["Gastos 🧾", "Paga y Comparte 🫂", f"{name} 👤"]
    
    styles = {
        "nav": {
            "background-color": "#72b1aa",
            "justify-content": "Center",
            "position": "relative",
            "top": "-5px",
            "z-index": "0",
            "width": "100%",
        },
        "img": {
            "padding-right": "14px",
            "z-index": "1",
        },
        "span": {
            "color": "white",
            "padding": "14px",
        },
        "active": {
            "color": "var(--text-color)",
            "background-color": "#a0e0d9",
            "font-weight": "normal",
            "padding": "14px",

        }
    }

    options = {
        "show_menu": True,
        "show_sidebar": True,
        "fix_shadow": True,
        "use_padding": True,
    }

    pag = st_navbar(
        pages,
        logo_path=logo_path,

        styles=styles,
        options=options,
        adjust=True
    )        

    if pag == "Home":
        summary_page(name, userId)
    elif pag == "Gastos 🧾":
        expenses_page(name, userId)
    elif pag == "Paga y Comparte 🫂":
        payshare_page(name)
    elif pag == f"{name} 👤":
        user_page(name)


if __name__ == "__main__":
    main()