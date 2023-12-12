import os
import pandas as pd
from colorama import init, Fore
from io import StringIO
import requests
init()

def remove_useless_columns(dataframe):
        useless_columns = ['Country_code', 'Country', 'WHO_region']
        dataframe = dataframe.drop(useless_columns, axis=1)
        return dataframe

def standarize_data(dataframe):
    # standarize dates
    dataframe['Date_reported'] = dataframe['Date_reported'].str.strip().str.replace('[.- ]', '/', regex=True)
    # validate dates
    valid_formats = dataframe['Date_reported'] == valid_dates.dt.strftime('%m/%d/%Y')
    dataframe = dataframe[valid_formats]

    # standarize numeric data
    numeric_columns = ['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
    conditions = (dataframe[numeric_columns] >= 0) & (dataframe[numeric_columns].astype(str).str.isdigit())
    dataframe = dataframe[conditions.all(axis=1)]
    return dataframe

class World:

    def get_world_file(self):
        while True:
            url = input("Enlace del Archivo de Fallecidos a Nivel Mundial (csv): ")

            response = requests.get(url)

            if response.status_code == 200:
                csv_data = StringIO(response.text)

                dataframe = pd.read_csv(csv_data)

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
    