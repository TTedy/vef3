from flask import Flask, render_template, url_for 

app = Flask(__name__)


vorulisti =  [
        {
            "id": 0,
            "nafn": "Leðursófi",
            "lysing": "Fallegur og þægilegur leðursófi sem hentar fyrir alla fjölskylduna.",
            "mynd": "mynd0.jpg",
            "verd":160000,
            "nanar":["Svartur","60 X 120 CM"],
            "flokkur":"sofi"
        },
        {
            "id": 1,
            "nafn": "Svefnsófi",
            "lysing": "Svefnsófi sem hentar fyrir lítil og nett rými.  Rosa gott að sofa í honum.",
            "mynd": "mynd1.jpg",
            "verd":140000,
            "nanar":["Grár","70 X 120 CM"],
            "flokkur":"sofi"
        },
        {
            "id": 2,
            "nafn": "Fataskápur",
            "lysing": "Ef þú átt mikið af fötum er þessi skápur akkúrat fyrir þig, einn tveir og bing bæng.",
            "mynd": "mynd2.jpg",
            "verd":75000,
            "nanar":["Hvítlakkað","80 X 60 X 180 CM"],
            "flokkur":"skapur"
        },
        {
            "id": 3,
            "nafn": "Þvottaskápur",
            "lysing": "Ef þú vilt hafa allt á hreinu og vel skipulagt þá er þetta skápurinn fyrir þig.",
            "mynd": "mynd3.jpg",
            "verd":50000,
            "nanar":["Hvítt","100 X 70 X 200 CM"],
            "flokkur":"skapur"
        },
                {
            "id": 4,
            "nafn": "Borðstofuborð",
            "lysing": "Stílhreint og fallegt borð inn á hvert heimili.",
            "mynd": "mynd4.jpg",
            "verd":50000,
            "nanar":["Hvíttlakkaður Askur","100 X 70 X 200 CM"],
            "flokkur":"bord"
        },
        {
            "id": 5,
            "nafn": "Barnaborð",
            "lysing": "Fyrir smáfólkið, nú geta allir föndrað og leikið sér við þetta fallega borð.",
            "mynd": "mynd5.jpg",
            "verd":30000,
            "nanar":["Hvítt","50 X 50 X 60 CM"],
            "flokkur":"bord"
        }
    ]

valmynd = [ {"url":'/',"hlekkur":"Heim"},
            {"url":'/flokkur/sofi',"hlekkur":"Sofar"},
            {"url":'/flokkur/bord',"hlekkur":"Borð"},
            {"url":'/flokkur/skap',"hlekkur":"Skapar"}
          ]



@app.route("/")
def index():
    return render_template("index.html", valmynd=valmynd,v=vorulisti)

@app.route("/flokkur/<nafn>")
def flokkur(nafn):
    return render_template("sita3.html",v=vorulisti,nafn=nafn,valmynd=valmynd) 

@app.route("/vara/<int:id>")
def vorur(id):
    for x in vorulisti:
        if x["id"] == id:
            nafn = x["nafn"]
            lysing = x["lysing"]
            mynd = x["mynd"]
            verd = x["verd"]
    return render_template("sita2.html",nafn=nafn,id=id,lysing=lysing,mynd=mynd,verd=verd,valmynd=valmynd)


#Dynamic route
@app.route("/sita2/<texti>")
def sita2():
        return render_template("sita2.html",)

@app.errorhandler(404)
def error(error):
    return render_template("error.html")

print("")
app.run(debug=True)