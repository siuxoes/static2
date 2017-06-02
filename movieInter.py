from flask import Flask
from flask import Response
from flask import render_template
from flask import request

app = Flask(__name__)

print()

listaPeliculasObject = []
addMore = True
nombreActores = []
times = 1
globalTexto = ""

headers = {'User-agent': 'Mozilla/5.0'}

# Main loop, clean this @Siuxoes
##while addMore:
##    actor = input("Introduce el nombre de un actor que desea buscar: ")
##    URL = "http://suggestqueries.google.com/complete/search?client=firefox&q="
##    URL +=actor.upper()
##    response = requests.get(URL, headers=headers)
##    result = json.loads(response.content.decode('utf-8'))
##    respuesta =input("Según Google, el primer resultado del actor introducido es: {0} , ¿es correcto? Si/No: ".format(result[1][0].upper()))
##    while respuesta.lower() not in ["si","no","s","n"]:
##        respuesta = input(
##            "Según Google, el primer resultado del actor introducido es: {0} , ¿es correcto? Si/No: ".format(
##                result[1][0].upper()))
##    if respuesta.lower() in ["si", "s"]:
##        nombreActores.append(result[1][0].upper())
##    if len(nombreActores) > 0:
##        print()
##        print("Listado de actores actuales: ")
##        lista = [[i, j] for i, j in enumerate(nombreActores)]
##        for x in lista:
##            x[0] += 1
##            print("{0} - {1}".format(str(x[0]),x[1]))
##        print()
##    if len(nombreActores) >= 2:
##        respuesta = input("¿Desea añadir más actores? Si / No ")
##        while respuesta.lower() not in ["si", "no", "s", "n"]:
##            respuesta = input("¿Desea añadir más actores? Si / No ")
##        if respuesta.lower() in ['n', 'no']:
##            addMore = not addMore

import urllib.request
import requests
import time

start_time = time.time()


def get_peoples_id(listaEntrada):
    listaSalida = []
    for persona in listaEntrada:
        persona = urllib.request.quote(persona)
        URL = "https://api.themoviedb.org/3/search/person?api_key=6571f3c9bf9f6be28a99b58842d35298&language=en-US&query=" + persona + "&page=1&include_adult=false"
        r = requests.get(URL)
        if r.ok:
            print("okey!")
        d = r.json()

        listaSalida.append(d["results"][0]["id"])
    return listaSalida


class movie():
    image_url = ""
    movie_id = ""
    movie_title = ""
    youtube = ""
    date_out = ""

    def __init__(self, image_url=""):
        self.image_url = image_url

def get_movie_details(peliculaEntrada):
    print(peliculaEntrada)
    URL = "https://api.themoviedb.org/3/movie/"+str(peliculaEntrada) +"/videos?api_key=6571f3c9bf9f6be28a99b58842d35298&language=en-US"
    print(URL)
    r = requests.get(URL)
    if r.ok:
        print("okey!")
        d = r.json()
        r.close()
        return d
    else:
        return -1

def get_movies_list(listaEntrada):
    global listaPeliculasObject
    listaSalida = []
    for actor_lista in listaEntrada:
        actor_lista = str(actor_lista)
        URL = url = "https://api.themoviedb.org/3/person/" + actor_lista + "?api_key=6571f3c9bf9f6be28a99b58842d35298&append_to_response=credits"
        r = requests.get(url)
        if r.ok:
            print("okey!")

        d = r.json()
        r.close()

        movies = d["credits"]["cast"]
        movies_dict = {}

        for x in movies:
            new_movie = movie()
            if x["poster_path"] is not None:
                new_movie.image_url = "http://image.tmdb.org/t/p/w300/" + str(x["poster_path"])
            else:
                new_movie.image_url = "https://islandpress.org/sites/default/files/400px%20x%20600px-r01BookNotPictured.jpg"
            new_movie.movie_title = x["original_title"]
            new_movie.movie_id = x["id"]
            

            listaPeliculasObject.append(new_movie)
            movies_dict[x["id"]] = x["original_title"]
        listaSalida.append(movies_dict)
    return listaSalida


# for x in listaPeliculas:
#     print(x)
def intersection_List(listaEntrada):
    return set(listaEntrada[0]).intersection(*listaEntrada)


print()
print("COINCIDENCIAS ENTRE LOS ACTORES:")
print()
seq = 1
for x in nombreActores:
    print(" " * 19 + str(seq) + "\t" + x)
    seq += 1
print()

seq = 1
print("PELICULAS: ")

print(globalTexto)


@app.route('/')
def my_form():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def my_form_post():
    global listaPeliculasObject
    listaPeliculasObject = []
    nueva_lista = []
    global globalTexto
    global seq
    text = request.form['text']
    text1 = request.form['text2']
    arraymio = [text, text1]
    listaIdActores = []
    listaPeliculas = []
    listaPeliculasComunes = []
    listaIdActores = get_peoples_id(arraymio)
    listaPeliculas = get_movies_list(listaIdActores)
    listaPeliculasComunes = intersection_List(listaPeliculas)
    goodThing = True
    for x in listaPeliculasComunes:
        for pelicula in nueva_lista:
            if pelicula.movie_id == x:
                goodThing = False
        if goodThing:
            for algo in listaPeliculasObject:
                if algo.movie_id == x:
                    resultado = get_movie_details(algo.movie_id)
                    if len(resultado["results"]) <= 0:
                        algo.youtube = ""
                    else:
                        algo.youtube = "https://www.youtube.com/embed/" + resultado["results"][0]["key"]
                    nueva_lista.append(algo)
                    break
        goodThing = True


    response = Response(globalTexto)
    response.headers["content-type"] = "text/plain"
    print(response)
    hola = ["tt", "cca"]
    return render_template('index.html', output=nueva_lista)


if __name__ == '__main__':
    app.run()
