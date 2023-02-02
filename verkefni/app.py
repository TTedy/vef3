from flask import Flask, render_template, url_for, json 
import urllib.request
from random import randint,choice
from datetime import date
import subprocess


app = Flask(__name__)

valmynd = [ {"url":'/',"hlekkur":"Heim"},
            {"url":'/hlekkur/Enskar',"hlekkur":"Enskar"},
            {"url":'/hlekkur/Íslenksar',"hlekkur":"Íslenksar"},
            {"url":'/hlekkur/Top-20',"hlekkur":"Top 20"},
          ]




@app.route("/")
def index():
    random_page = randint(1, 550)

    with urllib.request.urlopen("https://api.themoviedb.org/3/discover/movie?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&page="+ str(random_page)) as api:
        gogn = json.loads(api.read().decode())
    return render_template("index.html", myndir=gogn, valmynd=valmynd)

@app.route("/hlekkur/<nafn>")
def hlekkur(nafn):
    if nafn == "Enskar":
        with urllib.request.urlopen("https://api.themoviedb.org/3/discover/movie?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&with_original_language={}".format(nafn)) as api:
            hlekkur = json.loads(api.read().decode())
    if nafn == "Íslenksar":
        with urllib.request.urlopen("https://api.themoviedb.org/3/discover/movie?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&with_original_language={}".format(nafn)) as api:
            hlekkur = json.loads(api.read().decode())
    if nafn == "Top-20":
        pass
    return render_template("hlekkur.html", h=hlekkur,valmynd=valmynd)

@app.route("/mynd/<id>")
def mynd(id):
    with urllib.request.urlopen("https://api.themoviedb.org/3/movie/{}?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&language=is-IS".format(id)) as api:
        gogn = json.loads(api.read().decode())
        
        if gogn['overview'] == "":
            with urllib.request.urlopen("https://api.themoviedb.org/3/movie/{}?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&language=en-US".format(id)) as api:
                gogn = json.loads(api.read().decode())
    
    d = gogn['release_date']
    d = date.fromisoformat(d)
    d = (d.strftime("%#d.%#m.%Y"))

    with urllib.request.urlopen("https://api.themoviedb.org/3/movie/{}/videos?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&language=en-US".format(id)) as api:
        T = json.loads(api.read().decode())

    
    
    with urllib.request.urlopen("https://api.themoviedb.org/3/movie/{}/credits?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&language=en-US".format(id)) as api:
        c = json.loads(api.read().decode())

    return render_template("myndir.html", d = d, myndir=gogn, valmynd=valmynd, t=T, c=c)

@app.route("/Flokkar/<id>")
def flokkar(id):
    random_page = randint(1, 550)

    with urllib.request.urlopen("https://api.themoviedb.org/3/discover/movie?with_genres={}&api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&language=en-US&page="+str(random_page).format(id)) as api:
        genrasapi = json.loads(api.read().decode())

    print(id)
    return render_template("Flokkar.html",ga=genrasapi,valmynd=valmynd)

@app.errorhandler(404)
def error(error):
    return render_template("error.html")

app.run(debug=True)