import os
import pandas as pd
from colorama import init, Fore
from io import StringIO
init()

year = 2020

def is_positive_integer(value):
    try:
        return pd.notna(value) and int(value) >= 0
    except ValueError:
        return False

def is_valid_alpha(value):
    # Verifica si el valor contiene únicamente letras y espacios
    return all(char.isalpha() or char.isspace() for char in value)

def validate_alpha_columns(dataframe):
    # Aplica la función de validación a las columnas "departamento" y "municipio"
    condition = dataframe[['departamento', 'municipio']].applymap(is_valid_alpha).all(axis=1)

    # Filtra el DataFrame original
    dataframe = dataframe[condition]

    return dataframe


def is_valid_date_format(value):
    try:
        pd.to_datetime(value, format='%m/%d/%Y')
        return True
    except ValueError:
        return False

def standarize_data(dataframe):
    # filter valid date columns
    valid_date_columns = [col for col in dataframe.columns[5:] if is_valid_date_format(col)]

    # Get 2020 data
    dataframe = dataframe.drop(columns=[col for col in valid_date_columns if pd.to_datetime(col, format='%m/%d/%Y').year != year])

    # validate numeric data
    numeric_columns = dataframe.columns[4:]
    dataframe[numeric_columns] = dataframe[numeric_columns].fillna(0).replace('N/A', 0)
    condition = dataframe[numeric_columns].applymap(is_positive_integer).all(axis=1)
    dataframe = dataframe[condition]

    # standarize alphabetic data
    dataframe = validate_alpha_columns(dataframe)


    return dataframe




class Municipality:
    def get_municipality_file_path(self):
        while True:
            file_path = input(f"{Fore.YELLOW}Ruta del Archivo de Fallecidos por Municipio (csv): {Fore.RESET}")

            if not file_path.lower().endswith('.csv'):
                print(f"{Fore.RED}El archivo debe tener extensión .csv, intentalo de nuevo{Fore.RESET}")
                continue

            if os.path.isfile(file_path):
                return file_path
            else:
                print(f"{Fore.RED}El archivo no existe (o no es válido), intentalo de nuevo{Fore.RESET}")

    def clear_municipality_data(self, dataframe):
        # Remove duplicate registers
        print(f"{Fore.CYAN}Eliminando Registros Duplicados{Fore.RESET}")
        dataframe = dataframe.drop_duplicates()
        dataframe = dataframe.drop_duplicates(subset='codigo_municipio', keep='first')

        print(f"{Fore.CYAN}Eliminando datos irrelevantes para el análisis{Fore.RESET}")

        print(f"{Fore.CYAN}Estandarizando Campos Inválidos{Fore.RESET}")
        dataframe = standarize_data(dataframe)

        print(f"{Fore.CYAN}Manejando Datos Faltantes{Fore.RESET}")
        print(f"{Fore.GREEN}Limpieza de Datos por Municipio Realizada con Éxito{Fore.RESET}")
        return dataframe