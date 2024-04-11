import os
from dotenv import load_dotenv
import libsql_experimental as libsql

load_dotenv()

# Crear la conexión a la base de datos
TOKEN = os.environ.get('TOKEN_DB')
URL = os.environ.get('URL_DB')
NAME = os.environ.get('NAME_DB')
conn = libsql.connect(NAME, sync_url=URL, auth_token=TOKEN)
conn.sync()
