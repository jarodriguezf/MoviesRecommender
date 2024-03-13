import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler


# Los valores nulos de df_ los eliminaremos
def imputer_(df_):
    df_ratings_copy = df_.copy()
    df_ratings_copy=df_ratings_copy.dropna()

    return df_ratings_copy

# Eliminamos variable timestamp, tagId y relevance del dataset
def drop_variables(df_):
    df_ratings_copy = df_.copy()
    df_ratings_copy.drop(['timestamp'], axis=1, inplace=True)
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
# Extraemos  el genero de cada movieId (se considera al primero que aparece en genres antes de las '|')
def splitGenre_df_(df_):
    df_ratings_copy=df_.copy()
    # Extraemos el primer genero de la columna genres y lo almacenamos en una nueva variable
    df_ratings_copy['genre_split']=df_ratings_copy['genres'].apply(lambda x: x.split('|'))
    df_ratings_copy.drop('genres', axis=1, inplace=True)
    return df_ratings_copy

# Codificacion de categoricos a OneHotEncoder
def encoder_genre(df_):
    df_ratings_copy = df_.copy()
    # instancia del codificador
    encoder=MultiLabelBinarizer()
    encoded = pd.DataFrame(encoder.fit_transform(df_ratings_copy['genre_split']), columns=encoder.classes_, index=df_ratings_copy.index)
    df_ratings_copy.drop('genre_split', axis=1, inplace=True)
    result = pd.concat([df_ratings_copy, encoded], axis=1)
    
    return result

def normalizer(df_):
    df_ratings_copy = df_.copy()

    normalizer = MinMaxScaler()
    df_ratings_copy[['launch_year', 'rating']] = normalizer.fit_transform(df_ratings_copy[['launch_year', 'rating']])
 
    return df_ratings_copy


# Llamada que activa el procesamiento de todos los procesos
def united_functions(df_):
    print('INICIANDO PROCESAMIENTO DE DATOS...')
    print('- procesando tags y fusionando datasets..')
    #df_ = df_rating.merge(df_tag, how='right', on='movieId')
    df_=imputer_(df_)# Eliminamos los valores nulos
    print('- Eliminacion de nulos..')
    df_=drop_variables(df_)
    print('- Eliminando variables no necesarias...')
    df_=launchYear_title_df_(df_) # Extrae año del titulo
    print('- Extrayendo año del titulo...')
    list_user_movie=df_[['userId','movieId','rating','title']]# Almacenar valores originales (los usaremos en la comprobacion del recommender)
    print('- Almacenando en variable copia del df original...')
    df_=splitGenre_df_(df_)# extraemos generos
    print('- Extraemos los generos de cada pelicula...')
    df_.drop(['movieId', 'userId', 'title'], axis=1, inplace=True)
    print('- Eliminamos variables no necesarias...')
    df_=encoder_genre(df_)# Codificacion categoricas genres
    df_=normalizer(df_)
    print('- Codificamos los generos y normalizamos para su correcto formato...')
    print('FIN DE PROCESAMIENTO DE DATOS')

    return df_, list_user_movie