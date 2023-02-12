from flask import Flask, render_template, url_for, json, session, request
import urllib.request
from random import randint,choice
import datetime
from datetime import date,timedelta
import subprocess


app = Flask(__name__)
app.secret_key = "secret key"


valmynd = [ {"url":'/',"hlekkur":"Heim"},
            {"url":'/hlekkur/Myndir',"hlekkur":"Myndir í syningu"},
            {"url":'/hlekkur/Meðmelt',"hlekkur":"Best meðmelt"},
            {"url":'/hlekkur/Dramas',"hlekkur":"Best Dramas"},
          ]




@app.route("/")
def index():
    global random_page
    random_page = randint(1, 550)

    session.pop("page", None)  # clear the "page" session variable
    session["page"] = random_page  # set the "page" session variable

    with urllib.request.urlopen("https://api.themoviedb.org/3/discover/movie?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&page="+ str(random_page)) as api:
        gogn = json.loads(api.read().decode())
    return render_template("index.html", myndir=gogn, valmynd=valmynd)


@app.route("/page", methods=["POST"])
def update_page():
    global random_page
    
    if "page" not in session:
        session["page"] = random_page

    if request.form["page"] == "previous":
        session["page"] -= 1
    elif request.form["page"] == "next":
        session["page"] += 1
    
    page=session["page"]

    print()
    print()
    print(page)
    print()
    print()


    with urllib.request.urlopen("https://api.themoviedb.org/3/discover/movie?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&page="+ str(page)) as api:
        gogn = json.loads(api.read().decode())
    
    return render_template("index.html", myndir=gogn, valmynd=valmynd)







@app.route("/hlekkur/<nafn>")
def hlekkur(nafn):
    staðir = {"url_1":"https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&page=1","url_2":"https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&page=1","url_3":"https://api.themoviedb.org/3/discover/movie?primary_release_date.gte={}&primary_release_date.lte={}&api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&page=1"}
    x = datetime.date.today()
    old_x = x - timedelta(weeks=2)
    staðir["url_3"] = staðir["url_3"].format(old_x,x)
    mapping = {"Meðmelt":"url_1","Dramas":"url_2","Myndir":"url_3"}
    if nafn in mapping:
        key = mapping[nafn]
        apistað = staðir.get(key)

    with urllib.request.urlopen(apistað) as api:
        hlekkur = json.loads(api.read().decode())

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
        
    return render_template("Flokkar.html",ga=genrasapi,valmynd=valmynd)

@app.errorhandler(404)
def error(error):
    return render_template("error.html")

app.run(debug=True)