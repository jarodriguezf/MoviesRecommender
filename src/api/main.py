import streamlit as st
import pandas as pd

# Carga de datos (similitud del coseno ya calculada y lista de usuarios/peliculas)
df_simil_cosine= pd.read_csv("../modelling/cosine_csv/df_similCosineV2.csv")
list_user_movies= pd.read_csv("../../data/raw/data_model/final_data_used/list_user_moviesV2.csv")
# Diccionario de list_user_movies
dicc_user_movies = {'userId':list_user_movies['userId'], 'movieId':list_user_movies['movieId'], 'title':list_user_movies['title']}

# Buscar n usuarios 
def find_nusers(number):      
    lista =list_user_movies.head(number)
    lista.drop(['rating', 'title'], axis=1, inplace=True)
    return lista

# Buscar items de usuario especifico
def find_specific_user(userId):
    user=list_user_movies[list_user_movies['userId']==userId]
    if user.empty:
        return None
    return user

#========================================

# LOGICA RECOMENDACION

def comprobar_existencia(diccionario, movie_id, user_id):    
    for i in range(len(diccionario['userId'])):
        if diccionario['userId'].iloc[i] == user_id and diccionario['movieId'].iloc[i] == movie_id:
            return True
    return False

def obtener_index_movieId(diccionario, movie_id):
    for i in range(len(diccionario['movieId'])):
        if diccionario['movieId'].iloc[i]==movie_id:
            index = i
            break
    return index

def get_title_from_movieId(user_id ,diccionario):
    index = diccionario['userId'].loc[diccionario['userId'] == user_id].index
    # Obtén los títulos de las películas
    titles_saws = diccionario['title'].loc[index]
    return titles_saws

# Funcion de recomendacion para un usuario y pelicula
st.cache_data
def get_recommendations(user_id, movie_id,dicc_user_movies=dicc_user_movies, simil_cosine=df_simil_cosine, threshold=0.7):
    #Comprobamos que el usuario para la pelicula dada existe
    comprobar_user_movie_exist=comprobar_existencia(dicc_user_movies, movie_id, user_id)

    if comprobar_user_movie_exist:
       #Obtener indice de la pelicula dada
        index=obtener_index_movieId(dicc_user_movies, movie_id)

        # Obtén la lista de similitudes del coseno para una película y usuario dada
        cosine_sim_list = simil_cosine.iloc[index]

        # Ordena las películas en función de la similitud del coseno
        most_similar_movies_sorted=cosine_sim_list.sort_values(ascending=False)

        # Obtiene los índices de las 5 películas más similares superior al umbral 
        most_similar_movies = most_similar_movies_sorted[most_similar_movies_sorted > threshold][:5].index

        # Convertir los índices a enteros
        most_similar_movies_int = most_similar_movies.astype(int)

        # Obtiene los títulos de las películas más similares
        most_similar_movie_titles = list(set([dicc_user_movies['title'][id] for id in most_similar_movies_int if id in dicc_user_movies['title']]))

        # Obtener los titulos de todas las peliculas vistas por el usuario
        titles_saws = get_title_from_movieId(user_id ,dicc_user_movies)
        titles_saws = list(titles_saws)
        
        # Pelicula actual pasada por parametros (title)
        actual_title_index = dicc_user_movies['movieId'].loc[dicc_user_movies['movieId'] == movie_id].index[0]
        actual_title=dicc_user_movies['title'].loc[actual_title_index]
        
        # Filtra las películas recomendadas para excluir las que el usuario ya ha visto
        recommended_movies = [movie for movie in most_similar_movie_titles if movie not in titles_saws]

        # Si las peliculas se devuelven vacias se retorna la condicion
        if not recommended_movies:      
            st.write(':red[No se encontro una pelicula lo suficientemente significativa para recomendar]')
        else:
            st.markdown(f'Para el usuario con ID: **{user_id}**')
            st.markdown(f'Porque ha visto: **{actual_title}**')
            st.markdown(f'**RECOMENDAMOS:**')
            return recommended_movies
    else:
        st.write(':red[El usuario no ha visto la pelicula dada, no podemos recomendar sin un historial previo]')

#===============================================


# Crear la aplicación Streamlit
def main():
    st.title(":blue[Movies] Recommender :popcorn:")

    with st.form(key='form_finder_users_elements'):
        number_of_users = st.number_input("Ingrese el numero de usuarios a mostrar o el id de un usuario:", min_value=1)
        col1, col2 = st.columns(2)
        with col1:
            submit_button_list_users = st.form_submit_button("Mostrar lista de usuarios")
        with col2:
            submit_button_specific_user = st.form_submit_button("Mostrar elementos de un usuario")

    # Activa la busqueda de usuarios aleatoriamente
    if submit_button_list_users:
        lista=find_nusers(number_of_users)
        # Convertir las columnas a tipo entero
        lista[['userId','movieId']] = lista[['userId','movieId']].astype(int)
        st.table(lista)
        
    # Activa la busqueda de un usuario en concreta (mostrando su informacion)
    if submit_button_specific_user:
        user = find_specific_user(number_of_users)
        if user is None:
            st.write(':red[El id del usuario indicado no existe]')
        else:
            # Convertir las columnas a tipo entero
            user[['userId','movieId']] = user[['userId','movieId']].astype(int)
            st.table(user)


    with st.form(key='form_recommendation'):
        # Utilizar las variables almacenadas en st.session_state
        usuario_id_temp = st.number_input("Ingrese el ID del usuario:", min_value=1)
        pelicula_id_temp = st.number_input("Ingrese el ID de la película:", min_value=1)
        submit_button_recommender = st.form_submit_button("Obtener recomendaciones")

    if submit_button_recommender:
        # Mostramos las peliculas mas similares en funcion del contenido (generos, fecha y rating)
        recommendation=get_recommendations(usuario_id_temp, pelicula_id_temp)
        if isinstance(recommendation, list):
            for index,item in enumerate(recommendation):
                st.write(index+1,item)
           

if __name__ == "__main__":
    main()