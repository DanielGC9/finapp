import streamlit as st
from src.app.tabs import summary_page, categories_page


def home(expenses, income):
    # Page settings
    st.write("# :abacus: Expense Management",)

    # Tabs navigation
    tab1, tab2, tab3 = st.tabs(['Sumary', 'By Category', 'Debts'])

    with tab1:
        summary_page(expenses, income)
    with tab2:
        categories_page(expenses, income)
    with tab3:
        st.write("# Debts")

# with st.sidebar:
    #     selected = option_menu(None, ["Summary", "Categories"],
    #     icons=['house', "list-task"],
    #     menu_icon="cast", default_index=0, orientation="vertical",
    #     styles={
    #         "container": {"padding": "sidebar", "background-color": "#fafafa"},
    #         "icon": {"color": "black", "font-size": "15px"},
    #         "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "##1f66bd"},
    #         "nav-link-selected": {"background-color": "#1f66bd"},
    #     }
    #     )
    # if selected == "Summary":
    #     summary_page(expenses, income)
    # elif selected == "Categories":
    #     categories_page(expenses, income)
