import pyodbc

# Configura los detalles de conexión
server = 'FROI-PC\SQLEXPRESS'
database = 'covid-data'
trusted_connection = 'yes'  # Utiliza 'yes' para Windows Authentication
driver = '{SQL Server}'

# Cadena de conexión para Windows Authentication
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}'

def get_database_connection():
    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except Exception as e:
        print(f"Error de conexión: {str(e)}")
        return None
    
def execute_queries(db_conn, queries):
    for q in queries:
        execute_query(db_conn, q)

def execute_query(db_conn, query):
    try:
        cursor = db_conn.cursor()
        cursor.execute(query)
        db_conn.commit()
    except Exception as e:
        print(f"Ocurrió un error al insertar: {str(e)}")
        db_conn.rollback()
    else:
        cursor.close()