# python -m venv venv
# ./venv/Scripts/Activate.ps1
# pip install -r requirements.txt
# python structure.py
# deactivate

import pyodbc
import json
import os

# Configuración de la conexión a SQL Server
server = 'tu_servidor'
database = 'tu_base_de_datos'
username = 'tu_usuario'
password = 'tu_contraseña'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Conectar a la base de datos
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Obtener la lista de tablas
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
tables = [row.TABLE_NAME for row in cursor.fetchall()]

# Inicializar la estructura JSON
data = {}

for table in tables:
    # Obtener los 100 primeros registros de la tabla
    cursor.execute(f"SELECT TOP 100 * FROM {table}")
    rows = cursor.fetchall()
    
    # Obtener los nombres de las columnas
    columns = [column[0] for column in cursor.description]
    
    # Formatear los registros en una lista de diccionarios
    table_data = []
    for row in rows:
        row_dict = {columns[i]: row[i] for i in range(len(columns))}
        table_data.append(row_dict)
    
    # Añadir los registros a la estructura JSON
    data[table] = table_data

# Convertir la estructura a JSON
json_output = json.dumps(data, indent=4)

# Crear la carpeta "app_data" si no existe
output_dir = 'app_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Guardar el JSON en un archivo dentro de la carpeta "app_data"
output_file_path = os.path.join(output_dir, 'table_data.json')
with open(output_file_path, 'w') as json_file:
    json_file.write(json_output)

# Cerrar la conexión
cursor.close()
conn.close()

print(f"Datos de las tablas exportados a {output_file_path}")