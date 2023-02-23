from flask import Flask,render_template,request,session
# mikið import fyrir wtformið
import pyrebase
from pyrebase.pyrebase import Auth

from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,SubmitField,TextAreaField,IntegerField,HiddenField,DateField,PasswordField
from wtforms.validators import DataRequired, InputRequired, Length

from flask_ckeditor import CKEditor # import fyrir CKEditorinn, þurfum að vera búin að pip install flask-ckeditor


app = Flask(__name__)
app.config['SECRET_KEY'] = "gaman" # þurfum þetta fyrir csrf, samt hafa random
ckeditor = CKEditor(app)  # Frumstillum / smíðum ckeditor tilvik

valmynd = [ {"url":'/',"hlekkur":"Heim"},
            {"url":'/innskra',"hlekkur":"innskra"},
            {"url":'/dataform',"hlekkur":"Dataform"},
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
auth = fb.auth()


class Frm(FlaskForm):
    email = EmailField("Póstur:", validators=[InputRequired()])
    password = PasswordField("lykilord", validators=[InputRequired()])
    takki = SubmitField("skrá")

class Dataform(FlaskForm):
    nafn = StringField("nafn:",validators=[InputRequired()])
    flokkur = SelectField(u'Hvaða bolti', choices=[('Fotbolti', 'Fotbolti'), ('Handbolti', 'Handbolti'), ('Korfubolti', 'Korfubolti')])
    texti = TextAreaField("Texti:", validators=[InputRequired(),Length(min=5,max=15)])  # Birtum CKEditorinn í þessum í index.html
    mynd = StringField("url",validators=[InputRequired()])
    takki = SubmitField("innskra:")

@app.route('/')
def index():
    sg = bool()
    user = db.child("Gogn").get()
    getdata = dict(user.val())
    if  'notandi' in session and session['notandi']:
        try:
            return render_template("index.html",gd = getdata,valmynd=valmynd,sg = True)
        except:
            return render_template("index.html",gd = getdata,valmynd=valmynd,sg = True)
    else:
        return render_template("index.html",valmynd=valmynd,sg=False, gd = getdata)

@app.route('/dataform')
def df():
    # Tilvikið f af Frm klasanum ( sem er form ) sendur yfir í template
    return render_template("nyskra.html", df=Dataform(), valmynd=valmynd)

@app.route('/nyskra', methods=["GET","POST"])
def ns():
    df = Dataform()
    if request.form:
        flokkur = df.flokkur.data
        nafn = df.nafn.data
        mynd = df.mynd.data
        texti = df.texti.data

        try:
            db.child("Gogn").push({"flokkur":flokkur,"nafn":nafn,"texti":texti,"mynd":mynd})
            return render_template("index.html",valmynd=valmynd)
        except:
            return render_template("index.html",valmynd=valmynd)
    else:
        return render_template("index.html",valmynd=valmynd)
    # Tilvikið f af Frm klasanum ( sem er form ) sendur yfir í template
    return render_template("nyskra.html", df=Dataform(), valmynd=valmynd)

@app.route('/innskra')
def innskra():
    # Tilvikið f af Frm klasanum ( sem er form ) sendur yfir í template
    return render_template("innskra.html", f=Frm(), valmynd=valmynd)

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
            session['notandi'] = True 
            
            x = "Innskráning tóks..."
            user = db.child("Gogn").get()
            getdata = dict(user.val())
            
            return render_template("index.html",gd = getdata, x=x ,valmynd=valmynd)
        except:
            x = "Innskráning tóks ekki..."
            return render_template("index.html",x=x,valmynd=valmynd)
        
    else:
        x = "Má ekki, verðum að koma úr formi"
        return render_template("index.html",x=x,valmynd=valmynd )


@app.route('/utskra')
def utskra():
    if session:
        session.pop("notandi", None)
    return render_template("index.html",valmynd=valmynd )

if __name__ == "__main__":
    app.run(debug=True)