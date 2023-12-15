import os
import pandas as pd
import chardet
from colorama import init, Fore
from io import StringIO
import requests
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
    condition = dataframe[['Country']].applymap(is_valid_alpha).all(axis=1)

    # Filtra el DataFrame original
    dataframe = dataframe[condition]

    return dataframe


def remove_useless_columns(dataframe):
    useless_columns = ['WHO_region']
    dataframe = dataframe.drop(useless_columns, axis=1)
    return dataframe

def standarize_data(dataframe):

    # standarize dates
    dataframe['Date_reported'] = dataframe['Date_reported'].str.strip().str.replace('[-. ]', '/', regex=True)
    
    # validate dates
    valid_formats = pd.to_datetime(dataframe['Date_reported'], errors='coerce', format='%m/%d/%Y').notna()
    dataframe = dataframe[valid_formats]
    dataframe['Date_reported'] = pd.to_datetime(dataframe['Date_reported'], format='%m/%d/%Y')
    dataframe = dataframe[dataframe['Date_reported'].dt.year == year]

    # standarize numeric data
    numeric_columns = ['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']

    dataframe[numeric_columns] = dataframe[numeric_columns].fillna(0).replace('N/A', 0)
    # Filter rows where at least one numeric column is not a positive integer
    condition = dataframe[numeric_columns].applymap(is_positive_integer).all(axis=1)
    dataframe = dataframe[condition]

    # standarize alphabetic data
    # dataframe = validate_alpha_columns(dataframe)

    return dataframe



class World:

    def get_world_file(self):
        while True:
            url = input("Enlace del Archivo de Fallecidos a Nivel Mundial (csv): ")

            response = requests.get(url)

            if response.status_code == 200:
                result = chardet.detect(response.content)
                encoding = result['encoding']
                
                text = response.content.decode(encoding)
                data = StringIO(text)

                dataframe = pd.read_csv(data)

                return dataframe
            else:
                print(f"{Fore.RED}Hubo un error al descargar el archivo de la url {url}\nRevise que el enlace sea el correcto\nStatus: {response.status_code}{Fore.RESET}")

    def clear_world_data(self, dataframe):
        # Remove duplicate registes
        print(f"{Fore.CYAN}Eliminando Registros Duplicados{Fore.RESET}")
        dataframe = dataframe.drop_duplicates()

        # Remove useless data
        print(f"{Fore.CYAN}Eliminando datos irrelevantes para el análisis{Fore.RESET}")
        dataframe = dataframe[dataframe['Country_code'] == 'GT']
        dataframe = remove_useless_columns(dataframe)

        # Standarize data
        print(f"{Fore.CYAN}Estandariazando Campos Inválidos{Fore.RESET}")
        dataframe.replace('N/A', pd.NA, inplace=True)
        # Standarize date
        dataframe = standarize_data(dataframe)


        print(f"{Fore.CYAN}Manejando Datos Faltantes{Fore.RESET}")

        print(f"{Fore.GREEN}Limpieza de Datos Mundiales Realizada con Éxito (Se Obtuvo solamente datos de Guatemala){Fore.RESET}")
        return dataframe
    