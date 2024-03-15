<h1 align='center'>MoviesRecommender</h1>﻿

![portada2](https://github.com/jarodriguezf/MoviesRecommender/assets/112967594/845045b7-ab93-4911-8ba8-afdbf8c038c3)


*El proposito de este proyecto es replicar un sistema de recomendacion de peliculas. 
La idea de realizar dicho proyecto es la mejora y aprendizaje de nuevas areas de la IA.
Todo se ha realizado con objetivos didacticos, por tanto, no estamos ante un sistema profesional, ni tampoco con objetivos comerciales.*

## Estructura del proyecto :file_folder:.

![work_directory](https://github.com/jarodriguezf/MoviesRecommender/assets/112967594/3dabf405-f420-4f34-8399-406e7eda666d)

- data: Contiene lo referente a los datos, tanto en crudo como archivos de procesamiento.
  - exploratory: En esta carpeta se ha realizado el analisis eploratorio de los datos (se realizo con millones de registros).
  - model_design: Diseño del modelo (como estructuramos el algoritmo).
  - processed: Archivos de procesamiento de datos, en torno al eda aplicamos las transformaciones pertinentes (de forma manual).
  - raw: datasets (csv y parquets).
- src: Contiene archivos del modelado y el desarrollo de la web.
  - api: web que conecta con el modelo y los datos aportados.
  - baseline: Algoritmo simple para empezar a construir el modelo (no se utilizo).
  - modelling: archivos de procesamiento automatico (script que al llamarse ejecutan todas las funciones de procesamiento) y modelos (autoencoders y calculos). 

## Dataset 📄

Este proyecto utiliza el conjunto de datos MovieLens proporcionado por GroupLens (https://grouplens.org/).

Al utilizar este conjunto de datos, reconozco y acepto las condiciones de uso establecidas por GroupLens.

**Cita sugerida** ✒️

F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4, Article 19 (December 2015), 19 pages. [DOI=http://dx.doi.org/10.1145/2827872](http://dx.doi.org/10.1145/2827872)

**Aviso de No Endoso** 🚫

No se afirma ni se implica ningún respaldo por parte de la Universidad de Minnesota o el Grupo de Investigación GroupLens en relación con este proyecto. Este proyecto es de naturaleza didáctica y no tiene objetivos comerciales.

## Tecnologias usadas :computer:.

- Python (pandas, sklearn,numpy, tensorflow/keras).
- Librerias de visualizacion de datos (matplotlib, seaborn).
- Streamlit (para desarrollo web).
- Git (gitflow, como sistea de control de verisones).

## Funcionamiento de la App!! 🚀

La app trata de predecir en base a los contenidos de las peliculas otras con contenido similar, las caracteristicas usadas son:

- genero, año de lanzamiento y la puntuacion de los usuarios.
  
Encontramos una amplia gama de usuarios, algunos han visto mas de una pelicula y otros solo 1.

Cada prediccion que hagamos tendremos que pasar por parametros a la app el id del usuario y el id de la pelicula.

![portada](https://github.com/jarodriguezf/MoviesRecommender/assets/112967594/a8ddfaa7-b4f0-4374-b5fc-a9076a3cb45d)


**Observaciones:**
- Podemos ver la cantidad de usuarios junto con sus peliculas vistas que queramos.
  
![list_users](https://github.com/jarodriguezf/MoviesRecommender/assets/112967594/b30761b7-253a-417d-a742-b6e8d05c2fcb)

- Podemos tambien, mostrar las peliculas vistas por un usuario en concreto.

![find_user_item](https://github.com/jarodriguezf/MoviesRecommender/assets/112967594/73c7106b-ec26-42ca-a774-f103b36099e3)

- Si el usuario no ha visto una pelicula pasada por parametro, devolvera el error.

![user_not_movie](https://github.com/jarodriguezf/MoviesRecommender/assets/112967594/77ab24f4-3fd8-4290-b94c-5d17d814dc38)

- Si la pelicula no tiene una relevancia de mas de un 70% de similitud con otras peliculas, devolvera un error.

![relevancia_movie](https://github.com/jarodriguezf/MoviesRecommender/assets/112967594/7c598943-2a15-4ea2-849a-e58011cc59e6)

- En el caso de que encontremos un usuario correcto para una pelicula y relevancia significativa, mostrara en orden descendente otras peliculas nuevas similares.

![recomendation](https://github.com/jarodriguezf/MoviesRecommender/assets/112967594/ff9338c7-c02d-4fd8-bd1c-7b6d9a6f183c)




