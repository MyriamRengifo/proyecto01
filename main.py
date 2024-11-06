import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI

app = FastAPI()

data = pd.read_csv('data/data.csv') #cargamos el dataset
data

data['release_date'].apply(type)

data['release_date'] = pd.to_datetime(data['release_date'])

@app.get("/obtener_mes")
def cantidad_filmaciones_mes(mes):
    meses_indices = { #primero creamos un diccionario donde le asignamos un numero a cada mes 
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }
    mes = mes.lower()  #utilizamos .lower para que vuelva todas las letras minusculas y asi no hay problema de identificar que mes es, aunque use mayusculas al escribir el mes.
    numero_mes= meses_indices.get(mes) # se crea la variable numero_mes donde se usa get para identificar a que numero corresponde el mes insertado
    
    if numero_mes is None: # se crea la condición de que si el mes no es ninguno de los asignados, se devuelva que no es un mes. 
        return f'{mes} no es un mes'
    
    numero_peliculas_estrenadas = data[data['release_date'].dt.month == numero_mes] # se va a columna de release_date y se extra el mes de cada fila, el cual se compara con la variable numero_mes que tiene el numero del mes ingresado
    return f'{(len(numero_peliculas_estrenadas))} películas fueron estrenadas en el mes de {mes}' # se usa len para que se cuente el número de filas que coincidieron con el numero del mes ingresado.

@app.get("/obtener_dia")
def cantidad_filmaciones_dia(dia): 
    
    dias_indices = { #se utiliza la misma estructura de def cantidad_filmaciones_mes
        'domingo': 0,
        'lunes': 1,
        'martes': 2,
        'miercoles': 3,
        'jueves': 4,
        'viernes': 5,
        'sabado': 6
    }
    
    dia = dia.lower()  
    numero_dia= dias_indices.get(dia) 
    
    if numero_dia is None:
        return f'{dia} no es un día'
    
    numero_peliculas_estrenadas = data[data['release_date'].dt.dayofweek == numero_dia] # uno de los cambio es que se usa dayoftheweek para saber a que día de la semana corresponde. 
    return f'{(len(numero_peliculas_estrenadas))} películas fueron estrenadas en el día {dia}'

@app.get("/obtener_titulo_añoEstreno_popularidad")
def score_titulo(titulo_de_la_filmacion): # Se crea un función que acepta como unico parámetro el titulo de la producción
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower() # Se pone .lower para que vuelva el titulo minuscula
    titulo_pelicula = data[data['title'].str.lower() == titulo_de_la_filmacion] # a continuación se recorre la columna title
    # donde sus valores se ponen como minusculas nuevamente usando .lower para no tener problemas al comparar con el valor ingresado. 
    
    if not titulo_pelicula.empty: # si el titulo aparece en la columna 'title'
        titulo_pelicula = titulo_pelicula.sort_values(by= 'popularity', ascending= False).iloc[0] # Se filtra por la popularidad, esto debido a que
        # hay mas de una pelicula con el mismo nombre pero distintos datos. 
        estreno = titulo_pelicula['release_year'] # Una vez se filtra por la mas popular se busca el año de estreno que corresponde al titulo
        popularidad= titulo_pelicula['popularity'] # al igual que su popularidad.
        return f'La película {titulo_de_la_filmacion} fue estrenada en el año {estreno} con un score/popularidad de {popularidad}'
    else:
        return 'Título no encontrado.' #En caso de que el titulo no se encuentre entre los datos se devuelve lo siguiente. 
    
    
@app.get("/obtener_titulo_añoEstreno_numeroVotos_promedioVotos")
def votos_titulo(titulo_de_la_filmacion): #se utiliza la misma estructura de la función anterior
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    titulo_pelicula = data[data['title'].str.lower() == titulo_de_la_filmacion]
        
    if not titulo_pelicula.empty:
        titulo_pelicula = titulo_pelicula.sort_values(by= 'vote_count', ascending= False).iloc[0] #solo que en este caso filtramos por 'vote_count'
        votos = titulo_pelicula['vote_count']
        if votos < 2000: # se pone la condición de que la pelicula debe tener mas de 2000 valoraciones para aparecer.
            return f'La pelicula cuenta con menos de 2000 valoración' #de lo contrario se devuelve lo siguiente.
        else: 
            promedio_votos= titulo_pelicula['vote_average'] #Si la pelicula existe se busca su valor correspondiente en 'vote_average'
            estreno= titulo_pelicula['release_year'] # y en release_year
            return f'La película {titulo_de_la_filmacion} fue estrenada en el año {estreno}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}'
    else:
        return 'Título no encontrado.'

@app.get("/Obtener_actor")
def get_actor( nombre_actor ): # se creo la función get actor para obtener la información de un actor determinado
    
    # Lo primero que hacemos es utilizar la función apply y un función lambda para convertir los valores de la columna cast en listas,
    # esto debido a que se ven como listas pero son datos str con estructura de listas, aprovechando esta estructura usamos ast.literal_eval
    # para convertirlas. 
    data['cast'] = data['cast'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    #Una vez ya tenemos nuestras listas pasamos a volver minuscula el valor ingresado con la ayuda de .lower
    # esto con el fin de poder encontrar al actor incluso si su nombre se entrega en minuscula o mayuscula.
    nombre_actor = nombre_actor.lower() 
    # se crea otra variable actor donde se almacena otra función lambda la cual recorre los datos para buscar el nombre del actor, 
    # se pone punto lower para que en la comparación ambas esten en minusculas y no haya errores. Y se usa apply para que la función se ejecute en toda la columna cast.
    actor = data[data['cast'].apply(lambda x: nombre_actor in [actor.lower() for actor in x])]
    
    if not actor.empty: # se pone la condición de que si se encuentra al actor
        cantidad_peliculas = len(actor['title']) # se recorre la columna title para ver en que peliculas ha estado y se usa len para que devuelva en cuantas.
        retorno = actor['return'].sum() # se crea retorno y se usa .sum para que sume el retorno de todas las peliculas en las que ha estado
        promedio_retorno= retorno/ cantidad_peliculas # finalmente para sacar el promedio se usa la suma total del retorno
        # guardada en la variable retorno y se divide entre la cantidad de peliculas en las que ha participado. 
        return f'El actor {nombre_actor} ha participado en {cantidad_peliculas} filmaciones, el mismo ha conseguido un retorno de {retorno} con un promedio de {promedio_retorno} por filmación'
    else:
        return 'Actor no encontrado.' # si el actor no se encuentra se devuelve lo siguiente

# Modelo de Recomendación 

data_recomendado = data[['genres', 'production_companies', 'title', 'cast', 'crew']] # creamos un nuevo dataframe

def limpiar_espacios(columna): 
    return columna.apply(lambda x: ' '.join(str(x).split())) 
# creamos una función que toma por parametro las columnas del dataframe, utiliza el apply para aplicar a 
# cada fila la función de lambda la cual recorrera la fila y la separa con split separandolos por espacios
# vacios, despues de usa el join para concatenarlos.

#aplicamos la función en cada una de nuestras columnas y reemplazamos los valores en la columna original
data_recomendado.loc[:,'genres'] = limpiar_espacios(data_recomendado['genres']) #Usamos el .loc en cada una para que se reconozaca como el dataframe
data_recomendado.loc[:,'production_companies'] = limpiar_espacios(data_recomendado['production_companies'])# original y no una copia
data_recomendado.loc[:,'cast'] = limpiar_espacios(data_recomendado['cast'])
data_recomendado.loc[:,'crew'] = limpiar_espacios(data_recomendado['crew'])

# concatenamos toda la información en una columna llamada informacion, donde se concatenan dejando strings vacias para separar
data_recomendado['informacion'] = (
    data_recomendado['genres'].fillna('') + ' ' +
    data_recomendado['production_companies'].fillna('') + ' ' +
    data_recomendado['cast'].fillna('') + ' ' +
    data_recomendado['crew'].fillna('')
)

# una vez creada información se eliminan las columnas originales del dataframe
data_recomendado = data_recomendado.drop(columns=['genres', 'production_companies', 'cast', 'crew'])

# creamos parametros_vector y usamos CountVectorizer para vectorizar las palabras del dataframe e eliminar las palabras comunes con stop_words
parametros_vector = CountVectorizer(max_features=5000, stop_words='english')
vector = parametros_vector.fit_transform(data_recomendado['informacion']).toarray()
# usamos .fit_transform() tranforma los datos en una sola linea, se aplica a las filas de la columna información


numero_bloques = 500 #definimos el numero de elemento de los bloques donde se aplicara la similitud 
for i in range(0, len(vector), numero_bloques): # se usa un rango del indice 0 a la longitud del vector y se avanza cada 500 datos
    bloque = vector[i:i + numero_bloques] 
    similaridad_bloque = cosine_similarity(bloque) # se aplica la similitud del coseno a cada bloque

@app.get("/Obtener_recomendación_de_peliculas") 
def recomendacion(titulo: str): # creamos la función recomendación, se pone como condición que sea str
    titulo = titulo.lower() # se vuelve el titulo ingresado a minuscula
    titulo_minuscula = data_recomendado['title'].str.lower() # y tambien los valores del data frame
    #para que no se presenten problemas al comparar

    if titulo in titulo_minuscula.values: #iteramos en la columna buscando el titulo.
        try:
            indice = titulo_minuscula[titulo_minuscula == titulo].index[0] #se toma el primer valor igual
            distancia = sorted(list(enumerate(similaridad_bloque[indice])), reverse=True, key=lambda x: x[1])
            #buscamos la similitud entre las peliculas y se ordena de manera descendente de acuerdo a su similitud.
            peliculas_recomendadas = [data_recomendado.iloc[elemento[0]]['title'] for elemento in distancia[1:6]] 
            #Se crea una lista donde se almacenan los titulos similares y se hace una iteración con rango de [1:6] para
            # que no tome el titulo principal, es decir el indice 0 y termine al tener 5 valores. 
            return {"recomendaciones":peliculas_recomendadas} #se devuelven las peliculas recomendadas 
        except Exception as e:
            return {"error": f"El título '{titulo}' no se encuentra en los datos."} #sino le imprime lo siguientes.
