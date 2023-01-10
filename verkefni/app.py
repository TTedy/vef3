from flask import Flask, render_template, url_for 

app = Flask(__name__)

listi = ["Einn","Tveir","Þrír","Fjórir"]
titill = "Tölur"
lið = {"lið1":"Man U","lið2":"Liverpool","lið3":"Mac C"}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sita2")
def sita2():
        return render_template("sita2.html",listi=listi,titill=titill)

@app.errorhandler(404)
def error(error):
    return render_template("error.html")

print("")
app.run(debug=True)