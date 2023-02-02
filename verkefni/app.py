from flask import Flask, render_template, url_for, json 
import urllib.request
from random import randint,choice
from datetime import date


random_page = randint(1, 550)


with urllib.request.urlopen("https://api.themoviedb.org/3/discover/movie?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&page="+ str(random_page)) as api:
    gogn = json.loads(api.read().decode())


app = Flask(__name__)

valmynd = [ {"url":'/',"hlekkur":"Heim"},
            {"url":'/flokkur/',"hlekkur":"Enskar"},
            {"url":'/flokkur/',"hlekkur":"Íslenksar"},
            {"url":'/flokkur/',"hlekkur":"top 100"}
          ]



@app.route("/")
def index():
    return render_template("index.html", myndir=gogn, valmynd=valmynd)

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

@app.route("/myndir/<id>")
def flokkar(id):
    return render_template("Flokkar.html")

@app.errorhandler(404)
def error(error):
    return render_template("error.html")

app.run(debug=True)