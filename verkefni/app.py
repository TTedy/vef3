from flask import Flask,render_template,request,session
# mikið import fyrir wtformið
import pyrebase
from pyrebase.pyrebase import Auth

from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,SubmitField,TextAreaField,IntegerField,HiddenField,DateField,PasswordField
from wtforms.validators import DataRequired, InputRequired, Length


app = Flask(__name__)
app.config['SECRET_KEY'] = "gaman" # þurfum þetta fyrir csrf, samt hafa random


valmynd = [ {"url":'/',"hlekkur":"Heim"},
            {"url":'/nyskra',"hlekkur":"nykra"},
            {"url":'/innskra',"hlekkur":"innskra"},
            {"url":'/utskra',"hlekkur":"útskra"},
          ]



config = {
  "apiKey": "AIzaSyBRjWDZ1B4Jfc4U11Bt2Cw2ft-oLVZpHIc",
  "authDomain": "taekniskoli-48e6f.firebaseapp.com",
  "databaseURL": "https://taekniskoli-48e6f-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "taekniskoli-48e6f",
  "storageBucket": "taekniskoli-48e6f.appspot.com",
  "messagingSenderId": "627254874069",
  "appId": "1:627254874069:web:45363877c143d418f8375c",
  "measurementId": "G-DHK5VMK936"
}
fb= pyrebase.initialize_app(config)
db = fb.database()

class Dataform(FlaskForm):
    email = EmailField("Netfang:",validators=[InputRequired()])
    nafn = StringField("nafn:",validators=[InputRequired()])
    takki = SubmitField("innskra:")

@app.route('/')
def index():
    try:

        user = db.child("Gogn").get()
        getdata = dict(user.val())
        return render_template("index.html", gd = getdata)
    except:
        return "villa kom"

    return render_template("index.html",valmynd=valmynd)


@app.route('/dataform')
def df():
    # Tilvikið f af Frm klasanum ( sem er form ) sendur yfir í template
    return render_template("nyskra.html", df=Dataform(), valmynd=valmynd)

@app.route('/nyskra', methods=["GET","POST"])
def ns():
    df = Dataform()
    if request.form:
        email = df.email.data
        nafn = df.nafn.data
        try:
            db.child("Gogn").push({"email":email,"nafn":nafn})
            return "gögn eru komin!"
        except:
            return "að seta gögn virkaði ekki :("
    else:
        return "það má ekki koma nema úr formi!!"
    # Tilvikið f af Frm klasanum ( sem er form ) sendur yfir í template
    return render_template("nyskra.html", df=Dataform(), valmynd=valmynd)

if __name__ == "__main__":
    app.run(debug=True)