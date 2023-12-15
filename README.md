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
Solicita al usuario la ruta del archivo de fallecimientos por municipio y el enlace del archivo de fallecimientos a nivel mundial, los cuales son cargados y procesados en un dataset de pandas

2. Limpieza de Datos Mundiales:
Cada uno de los dataset es limpiado en funciones personalizadas, ya que cada dataset cuenta con una estructura diferente, dicha limpieza involucra varios filtros

3. Elimina duplicados y registros no relevantes.
Estandariza campos inválidos y maneja datos faltantes.

4. Valida que las fechas contengan el formato correspondiente, además de que los campos numéricos no posean valores negativos o alfabétios

5. Se realiza la transformación en la que el dataset de datos por municipio transforma su estructura de tal forma que sea compatible con la estructura del dataset de los casos de covid mundiales.

6. Después de esto se unen ambos dataset en base a la fecha y posteriormente son ingresados a una base de datos (SQL server) en bloques de 50 inserciones hasta llegar al total de inserciones

## Explicación del Modelo de Datos
### Modelo de Datos: COVID-19

#### Tabla: COUNTRY

- **code** (PK, varchar(5)) - Código del país.
- **name** (varchar(100)) - Nombre del país.

#### Tabla: COUNTRY_DEATHS

- **date** (PK, datetime) - Fecha.
- **country_code** (PK, FK to COUNTRY.code, varchar(5)) - Código del país.
- **new_cases** (int) - Nuevos casos.
- **cumulative_cases** (int) - Casos acumulados.
- **new_deaths** (int) - Nuevas muertes.
- **cumulative_deaths** (int) - Muertes acumuladas.

#### Tabla: DEPARTMENT

- **code** (PK, varchar(10)) - Código del departamento.
- **name** (varchar(100)) - Nombre del departamento.

#### Tabla: MUNICIPALITY

- **code** (PK, varchar(10)) - Código del municipio.
- **name** (varchar(100)) - Nombre del municipio.
- **department_code** (FK to DEPARTMENT.code, varchar(10)) - Código del departamento.
- **population** (int) - Población.

#### Tabla: MUNICIPALITY_DEATHS

- **municipality_code** (PK, FK to MUNICIPALITY.code, varchar(10)) - Código del municipio.
- **date** (PK, datetime) - Fecha.
- **total_deaths** (int) - Total de muertes.
- **day_deaths** (int) - Muertes del día en el país.

### Modelo de Datos Imagen
![Diagrama ER de Covid-data](./data/Diagrama%20ER.png)



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

