"""
    This module contains the main logic for the cron job
    that imports finance data from Notion to do a data analysis, 
    generates plots and pushes them to Notion.

    Created by: @DanielGuzman
    Date: 2023-06-08
    Version: 1.0.0
"""

import os
import sys
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from memory_profiler import profile



sys.path.append('.')
from src.utils.functions import import_data


@profile   
def grafica(data):
    # Graficar
    data['Date'] = pd.to_datetime(data['Date'])
    df_grouped = data.groupby(data['Date'].dt.date)['Amount'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped['Date'], df_grouped['Amount'], marker='o', linestyle='-')
    plt.title('Suma de Montos por Día')
    plt.xlabel('Día')
    plt.ylabel('Suma de Montos')
    plt.grid(True)
    plt.savefig('data/images/dayvsamount.png')


@profile#(stream=open('data/memory/main_cron.log', 'w'))
def main_function():

    # import the data to a dataframe
    data = import_data()
    grafica(data)

    df_grouped = data.groupby('Category')['Amount'].sum().reset_index()
    # Crear la figura con Plotly Express
    fig = px.pie(df_grouped, values='Amount', names='Category', title='Montos por Categoría')

    # Personalizar el diseño de la figura
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title=dict(font=dict(size=20)), 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)')

    # Guardar la imagen en formato PNG con fondo transparente
    fig.write_image('data/images/pie_px.png', format='png')
    # Mostrar la figura interactiva
    #fig.show()


if __name__ == "__main__":
    main_function()


