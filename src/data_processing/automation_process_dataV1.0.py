import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from datetime import datetime

# Almacena la ruta de los dataset correspondientes
df_=''

# Los valores nulos de df_ los modificaremos con el valor 0 y 'unknown'
def imputer_(df_):
    df_ratings_copy = df_.copy()
    
    # Columnas numéricas
    columns_numeric = ['userId', 'rating', 'timestamp']
    imp_numeric = SimpleImputer(strategy="constant", fill_value=0)
    df_ratings_copy[columns_numeric] = imp_numeric.fit_transform(df_ratings_copy[columns_numeric])

    # Columnas categóricas
    columns_categorical = ['title', 'genres']
    
    # Limpieza de valores nulos en columnas categóricas
    df_ratings_copy[columns_categorical] = df_ratings_copy[columns_categorical].fillna('unknown')

    # Imputación de valores constantes en columnas categóricas
    imp_categorical = SimpleImputer(strategy="constant", fill_value='unknown')
    df_ratings_copy[columns_categorical] = imp_categorical.fit_transform(df_ratings_copy[columns_categorical])

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

# Extraccion de categorioas en funcion rating
def valoration_df(df_):
    df_ratings_copy=df_.copy()
    # Gestionamos el rating en funcion de sus valores y añadimos cuatro categorias: 'excellent','good','bad','unknown'
    df_ratings_copy['valoration']=df_ratings_copy['rating'].apply(lambda x: 'excellent' if x == 5 else('good' if x >= 3 else ('unknown' if x == 0 else 'bad')))
    return df_ratings_copy


# Llamada que activa el procesamiento de todos los procesos
def united_functions(df_):
    df_= imputer_(df_)# llamada a funcion de limpieza de nulos 
    df_=timestamp_to_datetime_df_(df_) # Transforma timestamp a datetime (las fechas no valoradas se veran asi:"1970-01-01")
    df_=date_df_indepenDates(df_)# Extraemos fechas independientes
    df_=launchYear_title_df_(df_) # Extrae año del titulo
    df_=int_userId_df_(df_)# Convierte userId a entero
    df_=lenTitle_df_(df_) # Extraemos longitud del titulo
    df_=mainGenre_df_(df_) #Extraemos genero principal
    df_=valoration_df(df_)# Categorias en funcion de rating
    return df_

df_processed = united_functions(df_)