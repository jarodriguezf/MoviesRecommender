import pandas as pd
import numpy as np
from datetime import datetime


# Los valores nulos de df_ los eliminaremos
def imputer_(df_):
    df_ratings_copy = df_.copy()
    df_ratings_copy=df_ratings_copy.dropna()

    return df_ratings_copy

# Transformamos las variables del dataset 
# Timestamp, convertimos a datetime (referente a fecha de valoracion)
def timestamp_to_datetime_df_(df_):
    df_ratings_copy = df_.copy()
    # Convertimos el timestamp a datetime, luego aplicamos el formato año/mes/dia devolviendo un string
    df_ratings_copy['date_rating'] = df_ratings_copy['timestamp'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
    # Transformamos a Date el String
    df_ratings_copy['date_rating'] = df_ratings_copy['date_rating'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    # Eliminamos variable timestamp
    df_ratings_copy.drop('timestamp', axis=1, inplace=True)

    return df_ratings_copy

# Transformamos las variables del dataset df_
# date_rating, separamos año,mes y dia en variables independientes
def date_df_indepenDates(df_):
    df_ratings_copy = df_.copy()
    # Extraemos en variables sepadas el año, mes y dia de date_rating
    df_ratings_copy['year_rate'] = df_ratings_copy['date_rating'].dt.year
    df_ratings_copy['month_rate'] = df_ratings_copy['date_rating'].dt.month
    df_ratings_copy['day_rate'] = df_ratings_copy['date_rating'].dt.day
    # Eliminamos variable timestamp
    df_ratings_copy.drop('date_rating', axis=1, inplace=True)
    return df_ratings_copy

# Aleatoriamente modificamos 5 peliculas por usuario para simular que no la han visto.
def poner_no_vistas(grupo):

    # Número de películas a poner como no vistas
    num_no_vistas = min(10, len(grupo['movieId'].unique()))
    
    if num_no_vistas < 10:
        return grupo

    # Selecciona aleatoriamente algunas películas para poner como no vistas
    peliculas_no_vistas = np.random.choice(grupo['movieId'].unique(), size=num_no_vistas, replace=False)

    # Actualiza el grupo
    mask = grupo['movieId'].isin(peliculas_no_vistas)
    grupo.loc[mask, ['rating', 'year_rate', 'month_rate' ,'day_rate']] = 0
    
    return grupo

# Resetea el índice del DataFrame
def reset_grupo_index(df_):
    df_ = df_.reset_index(drop=True)
    return df_

# Transformamos las variables del dataset df_
# title, Extraemos el año de publicacion de cada pelicula en una variable nueva
def launchYear_title_df_(df_):
    df_ratings_copy = df_.copy()
    # Extraemos con expresiones regulares los años del title, rellenamos los nulos con 0 y casteamos a int
    df_ratings_copy['launch_year'] = df_ratings_copy['title'].str.extract(r'\((\d{4})\)', expand=False).fillna('0').astype(int)
    # Eliminamos el año y cualquier contenido entre paréntesis en la columna 'title'
    df_ratings_copy['title'] = df_ratings_copy['title'].apply(lambda x: x.split(' (')[0])
    return df_ratings_copy

# Transformamos las variables del dataset df_
# Convertimos userId a entero
def int_userId_df_(df_):
    df_ratings_copy=df_.copy()
    # Convertir 'userId' a int
    df_ratings_copy['userId'] = pd.to_numeric(df_ratings_copy['userId'], errors='coerce').astype('int64')
    return df_ratings_copy

# Transformamos las variables del dataset df_
# Extraemos la longitud de cada title y lo añadimos como nueva variable
def lenTitle_df_(df_):
    df_ratings_copy=df_.copy()
    #Extraemos la longitud de cada uno de los titulos
    df_ratings_copy['len_title']=df_ratings_copy['title'].apply(lambda x: len(x))

    return df_ratings_copy

# Transformamos las variables del dataset df_
# Extraemos  el genero principal de cada movieId (se considera principal al primero que aparece en genres antes del '|')
def mainGenre_df_(df_):
    df_ratings_copy=df_.copy()
    # Extraemos el primer genero de la columna genres y lo almacenamos en una nueva variable
    df_ratings_copy['main_genre']=df_ratings_copy['genres'].apply(lambda x: x.split('|')[0])
    return df_ratings_copy

# Transformamos las variables del dataset df_
# Extraemos el genero secundario de cada movieId (se considera secundario al segundo que aparece en genres antes del '|')
def secundaryGenre_df_(df_):
    df_ratings_copy=df_.copy()
    df_ratings_copy['secondary_genre'] = df_ratings_copy['genres'].apply(lambda x: x.split('|')[1] if len(x.split('|')) >1 else 'no_secundary')
    return df_ratings_copy

# Transformamos las variables del dataset df_
# Extraemos el genero tercero de cada movieId (se considera secundario al tercero que aparece en genres antes del '|')
def thirdGenre_df_(df_):
    df_ratings_copy=df_.copy()
    df_ratings_copy['third_genre'] = df_ratings_copy['genres'].apply(lambda x: x.split('|')[2] if len(x.split('|')) >2 else 'no_third')
    return df_ratings_copy

def valoration_df(df_):
    df_ratings_copy=df_.copy()
    # Gestionamos el rating en funcion de sus valores y añadimos cuatro categorias: 'excellent','good','bad','unknown'
    df_ratings_copy['valoration']=df_ratings_copy['rating'].apply(lambda x: 'excellent' if x == 5 else('good' if x >= 3 else ('unknown' if x == 0 else 'bad')))
    return df_ratings_copy

# Eliminar variables categoricas con ids ya definidos
def drop_columns(df_):
    df_ratings_copy=df_.copy()
    df_ratings_copy.drop(['title','genres','tag'], axis=1, inplace=True)
    return df_ratings_copy

# Llamada que activa el procesamiento de todos los procesos
def united_functions(df_):
    print("Entrando a united_functions (script de procesamiento de datos)")
    df_= imputer_(df_)# llamada a funcion de limpieza de nulos
    print("-Imputer realizado con exito_")
    df_=timestamp_to_datetime_df_(df_) # Transforma timestamp a datetime (las fechas no valoradas se veran asi:"1970-01-01")
    print("-Transformacion timestamp realizado con exito_")
    df_=date_df_indepenDates(df_)# Extraemos fechas independientes
    print("-Extraccion fechas realizado con exito_")
    df_=df_.groupby('userId').apply(poner_no_vistas)# Llamada a peliculas no vistas
    print("-Transformas pelculas no vista realizado con exito_")
    df_=reset_grupo_index(df_)# llamada a reset index
    print("-Reseteo indice realizado con exito_")
    df_=launchYear_title_df_(df_) # Extrae año del titulo
    print("-Extraccion año realizado con exito_")
    df_=int_userId_df_(df_)# Convierte userId a entero
    print("-Casteo a entero realizado con exito_")
    df_=lenTitle_df_(df_) # Extraemos longitud del titulo
    print("-Extraccion titulo realizado con exito_")
    df_=mainGenre_df_(df_) #Extraemos genero principal
    print("-Extraccion genero principal realizado con exito_")
    df_=secundaryGenre_df_(df_)#Extraemos genero secundario
    print("-Extraccion genero secundario realizado con exito_")
    df_=thirdGenre_df_(df_)#Extraemos genero terciario
    print("-Extraccion genero terciario realizado con exito_")
    df_=valoration_df(df_)# Categorias en funcion de rating
    print("-Extraccion valoracion rating realizado con exito_")
    df_=drop_columns(df_)#Eliminacion de 3 variables
    print("-Eliminacion columnas innecesarias realizado con exito_")
    print("--Fin del procesamiento de datos--")
    return df_