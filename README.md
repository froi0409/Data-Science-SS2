# Proyecto ETL
## Explicación del Proyecto:
Este proyecto de limpieza y análisis de datos tiene como objetivo procesar información relacionada con fallecimientos a nivel mundial y por municipio. Se divide en dos partes principales:
- Modulo World('world.py'):
-- Descarga y procesa datos de fallecimientos a nivel mundial.
-- Realiza limpieza de duplicados, eliminación de registros no relevantes y estandarización de campos inválidos.
-- Utiliza la clase World para encapsular la lógica y funciones relacionadas con los datos mundiales.

- Módulo Municipality('municipality.py')
-- Procesa datos de fallecimientos por municipio.
-- Realiza limpieza de duplicados, eliminación de registros no relevantes y estandarización de campos inválidos.
-- Utiliza la clase Municipality para encapsular la lógica y funciones relacionadas con los datos municipales.

- Módulo Principal ('main.py')
-- Coordinador principal del proyecto que orquesta la limpieza y análisis de datos tanto a nivel mundial como por municipio.

## Proceso de Limpieza de Datos
1. Selección de Archivos:
Solicita al usuario la ruta del archivo de fallecimientos por municipio y el enlace del archivo de fallecimientos a nivel mundial.
Carga de Datos:

2. Utiliza la biblioteca pandas para cargar los datos desde los archivos proporcionados.
Limpieza de Datos Mundiales:

3. Elimina duplicados y registros no relevantes.
Estandariza campos inválidos y maneja datos faltantes.
Limpieza de Datos por Municipio:

4. Elimina duplicados y registros no relevantes.
Estandariza campos inválidos y maneja datos faltantes.

## Explicación del Modelo de Datos
- Municipio:
-- Datos específicos relacionados con fallecimientos a nivel municipal.
Campos: 'departamento', 'codigo_departamento', 'municipio', 'codigo_municipio', 'población', y columnas de fechas

- Mundial:
-- Datos agregados a nivel mundial.
Campos: 'Date_reported', 'New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths'.

## Inicialización del Proyecto
1. **Permitir a Windows Ejecutar el Script:**
   ```bash
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
2. **Creación del Entorno Virtual:**
   ```bash
   python -m venv venv
3. **Ejecutar el Proyecto Principal:**
   ```bash
   python main.py

