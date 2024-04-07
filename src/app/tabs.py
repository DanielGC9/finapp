import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from matplotlib.colors import BoundaryNorm, ListedColormap
import plotly.express as px
from datetime import datetime
from src.utils.graphics_visuals import discrete_colorscale


def summary_page(df_expenses: pd.DataFrame, df_income: pd.DataFrame):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total Records',
                value=df_expenses.shape[0],
                delta='All expenses')
    col2.metric("Total Amount",
                value=f"{df_expenses['Amount'].sum():,.0f}$",
                delta='Total COP amount')
    col3.metric("Percentage",
                value=f"{df_expenses['Amount'].sum() / df_income['Amount'].sum() * 100:.2f}%",
                delta='Percentage spent')
    col4.metric("Income",
                value=f"{df_income['Amount'].sum():,.0f}$",
                delta='Total income COP')

    style_metric_cards(background_color='white', border_left_color='#1f66bd')

    st.markdown("""---""")

    div1, div2 = st.columns(2)
    with div1:
        st.header("Expenses")

        def pie(title, dataframe, x, y):
            fig = px.pie(dataframe, values=x, names=y, width=500, height=500)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, theme=None)

        pie('Income', df_expenses, 'Amount', 'Category')
    with div2:
        st.header("Bar Chart")

        def bar(title, dataframe, x, y):
            df = dataframe.groupby(x)[y].sum().reset_index(
            ).sort_values(by=y, ascending=False)
            fig = px.bar(df, x=x, y=y, width=500, height=500)
            # fig.update_traces(textposition='inside', textinfo='label')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, theme=None)

        bar('Income', df_expenses, 'Category', 'Amount')

    # Bar Chart
    st.header("Bar Chart")

    def bar(dataframe, x, y):
        df = dataframe.groupby([x, 'Category'])[y].sum(
        ).reset_index().sort_values(by=y, ascending=True)
        fig = px.bar(df, x=y, y=x, color='Category',
                     width=500, height=500, orientation='h')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    bar(df_expenses, 'Month', 'Amount')

    # Expenses Timeline
    st.header("Expenses Timeline")
    df_expenses.loc[:, 'Day'] = df_expenses['Date'].dt.day
    timeline_data = df_expenses[['Day', 'Category', 'Amount']]
    pivoted_data = pd.pivot_table(timeline_data,
                                  values='Amount',
                                  index='Category',
                                  columns='Day',
                                  aggfunc=sum)

    # Completing missing days (no expeses registered) with NaN
    days_month = np.arange(1, df_expenses['Date'].dt.days_in_month.iloc[0]+1)
    missing_days = [
        day for day in days_month if day not in pivoted_data.columns]

    for day in missing_days:
        pivoted_data[day] = pd.Series(dtype='int')

    pivoted_data = pivoted_data.reindex(sorted(pivoted_data.columns), axis=1)

    heatmap_colors = ['#a0e0d9', '#72b1aa', '#46847e', '#165954', '#00322e']
    # heatmap_colors = ['#a0e0d9', '#f9d38b', '#d1ac4f', '#f99893', '#ef516b']
    my_cmap = ListedColormap(heatmap_colors)
    limits = [0, 50000, 100000, 200000, 500000, 50e6]
    my_norm = BoundaryNorm(limits, ncolors=len(heatmap_colors))

    cell_size = 35
    row_title_width = 200
    width = cell_size*len(pivoted_data.columns)
    height = cell_size*len(pivoted_data.index)

    colorscale = discrete_colorscale(limits, heatmap_colors)

    fig = px.imshow(pivoted_data, color_continuous_scale=colorscale)

    for i in range(len(pivoted_data.columns)):
        fig.add_shape(type="line",
                      x0=0.5 + i,
                      y0=-0.5, x1=0.5 + i,
                      y1=len(pivoted_data.index) - 0.5,
                      line=dict(color="white", width=2))

    for i in range(len(pivoted_data.index)):
        fig.add_shape(type="line",
                      x0=-0.5,
                      y0=0.5 + i,
                      x1=len(pivoted_data.columns) - 0.5,
                      y1=0.5 + i, line=dict(color="white", width=2))
    st.plotly_chart(fig, use_container_width=True, theme=None)

    st.header("Table")
    st.dataframe(df_expenses, use_container_width=True)


def categories_page(df_expenses: pd.DataFrame, df_income: pd.DataFrame):
    st.write("# 💰 Categories")

    st.sidebar.header('Filters')
    category = st.sidebar.multiselect(
        'Select Category',
        options=np.append(['All'], df_expenses['Category'].unique()),
        default=['All']
    )

    if ['All'] == category:
        category = list(df_expenses['Category'].unique())

    pay_method = st.sidebar.multiselect(
        'Select Pay Method',
        options=np.append(['All'], df_expenses['PayMethod'].unique()),
        default=['All']
    )
    if ['All'] == pay_method:
        pay_method = list(df_expenses['PayMethod'].unique())

    start_date = st.sidebar.date_input(
        'Start Date',
        value=datetime.now().replace(day=1).date(),
    )

    end_date = st.sidebar.date_input(
        'End Date',
        value=datetime.now().date()
    )
    income_f = df_income.query('Date <= @end_date')

    expenses_f = df_expenses.query(
        'Category == @category & PayMethod == @pay_method & Date >= @start_date & Date <= @end_date'
    ).reset_index(drop=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total Records',
                value=expenses_f.shape[0],
                delta='All expenses')
    col2.metric("Total Amount",
                value=f"{expenses_f['Amount'].sum():,.0f}$",
                delta='Total COP amount')
    col3.metric("Percentage",
                value=f"{expenses_f['Amount'].sum() / income_f['Amount'].sum() * 100:.2f}%",
                delta='Percentage spent')
    col4.metric("Income",
                value=f"{income_f['Amount'].sum():,.0f}$",
                delta='Total income COP')

    style_metric_cards(background_color='white', border_left_color='#1f66bd')

    st.dataframe(expenses_f, use_container_width=True)
