from flask import Flask,render_template,request,session,flash
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
  "databaseURL": "",
  "authDomain": "taekniskoli-48e6f.firebaseapp.com",
  "projectId": "taekniskoli-48e6f",
  "storageBucket": "taekniskoli-48e6f.appspot.com",
  "messagingSenderId": "627254874069",
  "appId": "1:627254874069:web:45363877c143d418f8375c",
  "measurementId": "G-DHK5VMK936"
}
fb= pyrebase.initialize_app(config)
auth = fb.auth()

# Skilgreinum Form klasann og innsláttarsvæðin, erfir frá FlaskForm
class Frm(FlaskForm):
    email = EmailField("Póstur:", validators=[InputRequired()])
    password = PasswordField("lykilord", validators=[InputRequired()])
    takki = SubmitField("skrá")

@app.route('/')
def index():
    # Tilvikið f af Frm klasanum ( sem er form ) sendur yfir í template
    return render_template("index.html", f=Frm(), valmynd=valmynd)

@app.route("/nyskra")
def nykraupp():
    return render_template("nyskra.html", f=Frm(), valmynd=valmynd)

@app.route('/nyskra_vinnsla', methods=["POST", "GET"])
def gogn():
    # Förum bara hingað inn ef ýtt er á takkann úr forminu...
    if request.form:
        # tökum gögnin úr forminu og setjum í lista, sendum í template data.html
        fr = Frm()
        email = fr.email.data
        password = fr.password.data
        
        try:
            auth.create_user_with_email_and_password(email,password)
            x = "Nýskráning tóks..."
            return render_template("index.html",x=x)
        except:
            x = "Nýskráning tóks ekki..."
            return render_template("index.html",x=x)
        
    else:
        x= "Má ekki, verðum að koma úr formi"
        return render_template("index.html",x=x)


@app.route('/innskra')
def innskra():
    # Tilvikið f af Frm klasanum ( sem er form ) sendur yfir í template
    return render_template("innskra.html", f=Frm(), valmynd=valmynd )


@app.route('/display')
def display():
    # Retrieve the flash message from the user's session
    message = session.get('_flashes', None)
    return render_template('display.html', message=message)


@app.route('/innskraning_vinnsla', methods=["POST", "GET"])
def iv():
    # Förum bara hingað inn ef ýtt er á takkann úr forminu...
    if request.form:
        # tökum gögnin úr forminu og setjum í lista, sendum í template data.html
        fr = Frm()
        email = fr.email.data
        password = fr.password.data
        
        try:
            notandi = auth.sign_in_with_email_and_password(email,password)
            notandi_nanar = auth.get_account_info(notandi['idToken'])
            print(notandi_nanar)
            session['notandi'] = True 
            
            x = "Innskráning tóks..."
            return render_template("index.html",x=x)
        except:
            x = "Innskráning tóks ekki..."
            return render_template("index.html",x=x)
        
    else:
        x = "Má ekki, verðum að koma úr formi"
        return render_template("index.html",x=x)

@app.route('/utskra')
def utskra():
    session.pop("notandi", None)
    return "Þú ert útskráður"


@app.route('/admin')
def admin():
    try:
        if session['notandi'] == True:
            return render_template("admin.html")
    except:
        x = "þetta gett ekki" 
        return render_template("index.html",x=x)


#render_template("data.html", d=d),

if __name__ == "__main__":
    app.run(debug=True)