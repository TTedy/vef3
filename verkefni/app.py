from flask import Flask, render_template, url_for, json 
import urllib.request
from random import randint,choice

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
    return render_template("index.html", myndir=gogn)

@app.route("/mynd/<id>")
def mynd(id):
    return render_template("index.html", myndir=gogn)

@app.errorhandler(404)
def error(error):
    return render_template("error.html")

app.run(debug=True)