from flask import Flask, render_template, url_for 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sita2")
def sita2():
        return render_template("sita2.html")

@app.errorhandler(404)
def error(error):
    return render_template("error.html")


app.run(debug=True)