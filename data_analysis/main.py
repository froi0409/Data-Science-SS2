
import os
import time

import pandas as pd
from colorama import init, Fore

from config import db_config

from municipality import Municipality
from world import World


# init colorama
init()
os.system("cls")
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

def pause():
    print('Presiona una tecla para continuar...')
    input()

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
    time.sleep(2)
    os.system("cls")

    print(f"{Fore.YELLOW}Limpiando Data de Municipios{Fore.RESET}")
    municipality_data = municipality.clear_municipality_data(municipality_data)
    print(municipality_data)
    pause()

    print(f"{Fore.YELLOW}Limpiando Data de Municipios{Fore.RESET}")
    world_data = world.clear_world_data(world_data)
    print(world_data)
    pause()
    