from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/prufa")
def prufa():
    return "prufa"

@app.route("/ummig")
def ummog():
    return "þoavldur Breki"



app.run(debug=True)