### Descripción
Este proyecto tiene como objetivo analizar los datos sobre diferentes peliculas que van desde antes de 1990 hasta despues de 2020 teniendo en cuenta a disintos facotres como a que colección de peliculas pertenecen, su presupuesto, los generos que maneja, su cast, entre otras variables. 

### Tabla de contenido
1. [Introducción](#introducción)
2. [Instalación y Requisitos](#instalación-y-requisitos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Datos y Fuentes](#datos-y-fuentes)
5. [Metodología](#metodología)

### Instalación y Requisitos
**Requisitos:**
- Python 3.11 o menor
- pandas
- numpy
- matplotlib
- scikit-learn
- seaborn
**Pasos de instalación:**
1. Clonar el repositorio: `git clone https://github.com/MyriamRengifo/proyecto01.git`
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Instalar las dependencias: `pip install -r requirements.txt`

### Estructura del Proyecto
- `data/`: Contiene el archivo data.csv el cual se uso para las funciones y el modelo de recomendación
- `notebooks/`: Jupyter notebooks con la limpieza de datos ETL y el análisis EDA.
- `main.py`: Contiene el código utilizado para las funciones y el modelo de recomendación 
- `requirements.txt`: Contiene todas las librerias usadas en el proyecto 
- `README.md`: Documentación.

### Datos y Fuentes
Como fuente principal se usaron dos datasets con mas de 45000 peliculas y sus caracteristicas para su análisis. 

### Metodología
Se realizaron 5 funciones con el fin de entender la relación entre distintas variables. Tambien se realizo un modelo de recomendación usando la teoria del coseno para conocer las distancias entra las similitudes de las peliculas dentro del dataset, entre otros procesos. 

### Autor
Myriam Rengifo