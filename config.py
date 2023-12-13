import pyodbc

# Configura los detalles de conexión
server = 'FROI-PC\SQLEXPRESS'
database = 'covid-data'
trusted_connection = 'yes'  # Utiliza 'yes' para Windows Authentication
driver = '{SQL Server}'

# Cadena de conexión para Windows Authentication
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}'

# Intenta establecer la conexión
try:
    connection = pyodbc.connect(connection_string)
    print("Conexión exitosa")

    # Puedes agregar aquí tus operaciones en la base de datos

except Exception as e:
    print(f"Error de conexión: {str(e)}")
finally:
    # Cierra la conexión al finalizar
    if connection:
        connection.close()