from flask import Flask, render_template, url_for, json 
import urllib.request


with urllib.request.urlopen("https://api.themoviedb.org/3/discover/movie?api_key=2f4ea61d9bfaa42c92e84e4e34bd154b&page=1") as api:
    gogn = json.loads(api.read().decode())

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", myndir=gogn)


@app.errorhandler(404)
def error(error):
    return render_template("error.html")

app.run(debug=True)