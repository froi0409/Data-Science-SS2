
import os
import time
import numpy

import pandas as pd
from colorama import init, Fore

from config import get_database_connection, execute_queries, execute_query
from municipality import Municipality
from world import World
from query import insert_country, insert_department, insert_municipality


# init colorama
init()
os.system("cls")

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

def pause():
    print('Presiona una tecla para continuar...')
    input()

def transformation(municipality_data, world_data):
    # Obtener las fechas a partir de la columna 5
    fechas = municipality_data.columns[5:]

    # Convertir el DataFrame de formato ancho a largo usando melt
    municipality_data_long = pd.melt(municipality_data, id_vars=['departamento', 'codigo_departamento', 'municipio', 'codigo_municipio', 'poblacion'], value_vars=fechas, var_name='fecha', value_name='casos')

    # Convertir la columna 'fecha' al formato correcto
    municipality_data_long['fecha'] = pd.to_datetime(municipality_data_long['fecha'], format='%m/%d/%Y')

    # Ordenar el DataFrame
    municipality_data_long = municipality_data_long.sort_values(by=['departamento', 'municipio', 'fecha'])

    # Restablecer el índice
    municipality_data_long = municipality_data_long.reset_index(drop=True)

    # Convertir la columna 'Date_reported' de world_data al formato de fecha
    world_data['Date_reported'] = pd.to_datetime(world_data['Date_reported'], format='%Y-%m-%d')

    # Renombrar columnas para que coincidan con las del otro DataFrame
    world_data = world_data.rename(columns={'New_cases': 'new_cases_world', 'Cumulative_cases': 'cumulative_cases_world', 'New_deaths': 'new_deaths_world', 'Cumulative_deaths': 'cumulative_deaths_world'})

    # Combinar los DataFrames basándonos en la columna 'Date_reported' y 'fecha'
    combined_data = pd.merge(municipality_data_long, world_data, left_on='fecha', right_on='Date_reported', how='left')

    # Eliminar la columna 'Date_reported'
    combined_data = combined_data.drop('Date_reported', axis=1)

    # Convertir las columnas a valores enteros
    # Rellenar NaN con 0 antes de la conversión
    combined_data['cumulative_cases_world'] = combined_data['cumulative_cases_world'].fillna(0).astype(int)
    combined_data['cumulative_deaths_world'] = combined_data['cumulative_deaths_world'].fillna(0).astype(int)

    return combined_data

def insert_final_data(final_data):
    print('')

def insert_municipalities(municipality_data):
    print('')

def insert_countries(world_data):
    countries = world_data[['Country_code', 'Country']]
    countries = countries.drop_duplicates()

    # insert data
    try:
        conn = get_database_connection()
        for index, row in countries.iterrows():
            country_code = row['Country_code']
            country_name = row['Country']

            query = f"INSERT INTO COUNTRY (code, name) VALUES ('{country_code}', '{country_name}')"
            execute_query(conn, query)
            print("Se realizó con éxito la inserción de paises")
    except Exception as e:
        print(f"Ocurrió un error al ejecutar la conexión")
    finally:
        conn.close()
    
def insert_departmens(municipality_data):
    departments = municipality_data[['codigo_departamento','departamento']]
    departments = departments.drop_duplicates()

    # insert data
    try:
        conn = get_database_connection()
        for index, row in departments.iterrows():
            department_code = row['codigo_departamento']
            department_name = row['departamento']

            query = f"INSERT INTO DEPARTMENT (code, name) VALUES ('{department_code}', '{department_name}')"
            execute_query(conn, query)
    except Exception as e:
        print(f"Ocurrió un error al ejecutar la inserción del departamento")
    finally:
        conn.close()

def insert_municipalities(municipality_data):
    selected_columns = ['codigo_departamento', 'codigo_municipio', 'municipio', 'poblacion']
    municipalities = municipality_data[selected_columns]
    municipalities = municipalities.drop_duplicates(subset=['codigo_municipio', 'municipio'])

    try: 
        conn = get_database_connection()
        for index, row in municipalities.iterrows():
            municipality_code = row['codigo_municipio']
            municipality_name = row['municipio']
            municipality_department_code = row['codigo_departamento']
            municiaplity_population = row['poblacion']

            query = f"INSERT INTO MUNICIPALITY (code, name, department_code, population) VALUES ('{municipality_code}', '{municipality_name}', '{municipality_department_code}', '{municiaplity_population}')"
            execute_query(conn, query)

    except Exception as e:
        print("Ocurrió un error al ejecutar la inserción de un municipio")
    finally:
        conn.close()

def insert_departments_municipalities(municipality_data):
    insert_departmens(municipality_data)
    insert_municipalities(municipality_data)

def insert_data(municipality_data, world_data, final_data):
    insert_countries(world_data)
    insert_departments_municipalities(municipality_data)
    insert_final_data(final_data)

municipality = Municipality()
world = World()

# Read Municipality Data
by_municipality_csv = municipality.get_municipality_file_path()
municipality_data = pd.read_csv(by_municipality_csv)
os.system("cls")

print(f"{Fore.LIGHTGREEN_EX}El archivo {by_municipality_csv} fue seleccionado con éxito{Fore.RESET}")

# Download 
world_data = world.get_world_file()
if world_data is not None:
    print(f"{Fore.LIGHTGREEN_EX}La data se ha leído con éxito{Fore.RESET}")
    pause()
    os.system("cls")

    print(f"{Fore.YELLOW}Limpiando Data de Municipios{Fore.RESET}")
    municipality_data = municipality.clear_municipality_data(municipality_data)
    print('Municipality Data')
    print(municipality_data)
    pause()

    print(f"{Fore.YELLOW}Limpiando Data de Municipios{Fore.RESET}")
    world_data = world.clear_world_data(world_data)
    print('World Data')
    print(world_data)
    pause()

    print(f"{Fore.YELLOW}Transformando Data{Fore.RESET}")
    final_data = transformation(municipality_data, world_data)
    print(f"{Fore.LIGHTGREEN_EX}La data se ha transformado con éxito{Fore.RESET}")
    print(final_data)

    insert_data(municipality_data, world_data, final_data)

    pause()