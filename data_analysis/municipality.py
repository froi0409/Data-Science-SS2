import os
import pandas as pd
from colorama import init, Fore
from io import StringIO
init()

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

        print(f"{Fore.CYAN}Eliminando datos irrelevantes para el análisis{Fore.RESET}")

        print(f"{Fore.CYAN}Estandarizando Campos Inválidos{Fore.RESET}")
        dataframe.replace('N/A', pd.NA, inplace=True)

        print(f"{Fore.CYAN}Manejando Datos Faltantes{Fore.RESET}")
        print(f"{Fore.GREEN}Limpieza de Datos por Municipio Realizada con Éxito{Fore.RESET}")
        return dataframe