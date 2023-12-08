import psycopg2
import os
import time

import pandas as pd
import requests

from colorama import init, Fore
from io import StringIO
from config import db_config

# init colorama
init()
os.system("cls")

def get_municipality_file_path():
    while True:
        file_path = input(f"{Fore.YELLOW}Ruta del Archivo de Fallecidos por Municipio (csv): {Fore.RESET}")

        if not file_path.lower().endswith('.csv'):
            print(f"{Fore.RED}El archivo debe tener extensión .csv, intentalo de nuevo{Fore.RESET}")
            continue

        if os.path.isfile(file_path):
            return file_path
        else:
            print(f"{Fore.RED}El archivo no existe (o no es válido), intentalo de nuevo{Fore.RESET}")

def get_world_file():
    url = input("Enlace del Archivo de Fallecidos a Nivel Mundial (csv): ")

    response = requests.get(url)

    if response.status_code == 200:
        csv_data = StringIO(response.text)

        dataframe = pd.read_csv(csv_data)

        return dataframe
    else:
        print(f"{Fore.RED}Hubo un error al descargar el archivo de la url {url} - {response.status_code}{Fore.RESET}")
        return None

# Read Municipality Data
by_municipality_csv = get_municipality_file_path()
municipality_data = pd.read_csv(by_municipality_csv)
os.system("cls")

print(f"{Fore.LIGHTGREEN_EX}El archivo {by_municipality_csv} fue seleccionado con éxito{Fore.RESET}")

# Download 
world_data = get_world_file()
if world_data is not None:
    print(f"{Fore.LIGHTGREEN_EX}La data se ha leído con éxito{Fore.RESET}")
    time.sleep(2)
    os.system("cls")

    