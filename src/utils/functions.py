"""
In this module, you can find functions that 
are used in other modules.

Created by: @DanielGuzman
Date: 2023-06-01
"""
import os
import re
import requests
from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st


def create_dataframe(data)-> pd.DataFrame:
    """
    The function `create_dataframe` extracts data from records and creates a Pandas DataFrame with
    specific columns.

    Args:
      data: It looks like the code you provided is a function that takes in a parameter `data` and
    creates a Pandas DataFrame from the data extracted from the records in the input data.

    Returns:
      The function `create_dataframe(data)` is returning a Pandas DataFrame that contains extracted data
    from the input `data`. The data is extracted from the 'results' key in the input data and then
    converted into a structured format suitable for a Pandas DataFrame. The extracted data includes
    columns for 'Date', 'Name', 'Category', 'Amount', and 'Pay_Method'. Each row in the DataFrame
    corresponds
    """

    # Extraer los datos de los registros
    records = data['results']
    
    # Convertir los datos en un formato adecuado para un DataFrame de Pandas
    records_data = []
    for record in records:
        date_str = record['properties']['Date'].get('date', {}).get('start', None)
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = None
        
        name = record['properties']['Name'].get('title', [{}])[0].get('plain_text', None)
        category = record['properties']['Cat'].get('formula', {}).get('string', '').lstrip('@')
        amount = record['properties']['Amount'].get('number', None)
        
        pay_method_list = record['properties']['Método de pago'].get('multi_select', [])
        if pay_method_list:
            pay_method = pay_method_list[0].get('name', None)
        else:
            pay_method = None
        
        row = {
            'Date': date,
            'Name': name,
            'Category': category,
            'Amount': amount,
            'PayMethod': pay_method
        }
        records_data.append(row)

    return pd.DataFrame(records_data)

def import_data() -> pd.DataFrame:
    """
    The function `import_data` retrieves data from a Notion database using the Notion API and returns it
    as a pandas DataFrame.

    Returns:
      A pandas DataFrame containing the data from the Notion database is being returned.
    """
    TOKEN = os.environ.get('NOTION_TOKEN')
    DATABASE_ID = os.environ.get('DATABASE_ID')
    # URL base para las solicitudes a la API de Notion
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

    # Encabezados de la solicitud con el token de integración
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json",
        "Notion-Version" : "2022-06-28",
    }
    # Realizar una solicitud GET para leer los registros de la base de datos
    response = requests.post(url, headers=headers)
    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # Los datos de los registros estarán en la respuesta en formato JSON
        data = response.json()
        df = create_dataframe(data)
        return df
            
    else:
        return print('Error:', response.status_code)
    

def pie(title, dataframe, x, y):
    fig = px.pie(dataframe, values=x, names=y, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(legend_title='Categories', legend_y=0.5)
    st.plotly_chart(fig, use_container_width=True, theme=None)


def validate_email(email):
    """
    This function validates if an email is valid
    """
    patern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(patern, email):
        return True
    else:
        return False

def validate_username(user):
    """
    This function validates if an username is valid
    """
    patern = r'^[a-zA-Z0-9._+-]{6,}$'

    if re.match(patern, user):
        return True
    else:
        return False