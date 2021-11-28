# import sqlite3
# from sqlite3.dbapi2 import Cursor
import os
from ns import best
import os
from lastfile import last
from RIS import ris
from bokeh.layouts import row
from bokeh.embed import components
from CODE import first
from varMargin import var_pchange
import pandas as pd
from gold import gold_comp
# from werkzeug.utils import secure_filename
from flask import Flask, render_template,request,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query


# currentlocation=os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
allname=[]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['UPLOAD_FOLDER']='C://Users//AMIT//OneDrive//Desktop//PROJECT//static'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class user(db.Model):
    Uid = db.Column(db.Integer, primary_key=True)
    Uusername = db.Column(db.String(80))
    Uemail = db.Column(db.String(120))
    Upassword = db.Column(db.String(80))


@app.route('/', methods=['GET', 'POST'])
def register():
    if(request.method=='POST'):
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        
       

        
        if len(email) < 2:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        
        elif len(password) < 2:
            flash('Password must be at least 7 characters.', category='error')
        else:
            register = user(Uusername = name, Uemail = email, Upassword = password)
            db.session.add(register)
            db.session.commit()
            flash('Congratulation Account Created!!', category='sucessful')
            
            
            return redirect("/login")
        return redirect('/register')


    else:
        return render_template("register.html")


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["email"]
        passw = request.form["password"]
        
        login = user.query.filter_by(Uemail=uname, Upassword=passw).first()
        if login is not None:
            flash('Login sucessfully', category='sucessful')
            return redirect('/home')
        else:
            flash('Incorrect mail or password.', category='error')
            return render_template("login.html")

    return render_template("login.html")


 
@app.route('/home', methods=['GET','POST'])
def home():
    if(request.method=='POST'):
        f=request.files['file']
        
        df=pd.read_csv(f)
        global allname
        allname=df.symbol.unique()
        k=first(df)
        # b,l=best()
        var=var_pchange(df)
        gr = ris(df)
        allg=last(df)

        
        # if f.filename != '':
            
            # f.filename='user.csv'
            # f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        
        
        
        demo_script_code1,chart_code1=components(k)
        # demo_script_code2,chart_code2=components(f)
        # demo_script_code3,chart_code3=components(b)
        demo_script_code4,chart_code4=components(var)
        # demo_script_code5,chart_code5=components(RIS_1)
        # demo_script_code6,chart_code6=components(RIS_2)
        demo_script_code7,chart_code7=components(gr)
        demo_script_code8,chart_code8=components(allg)
       


        
        
        return render_template('home.html',
        demo_script_code1=demo_script_code1,chart_code1=chart_code1,
        # demo_script_code2=demo_script_code2,chart_code2=chart_code2,
        # demo_script_code3=demo_script_code3,chart_code3=chart_code3,
        demo_script_code4=demo_script_code4,chart_code4=chart_code4,
        # demo_script_code5=demo_script_code5,chart_code5=chart_code5,
        # demo_script_code6=demo_script_code6,chart_code6=chart_code6,
        demo_script_code7=demo_script_code7,chart_code7=chart_code7,
        demo_script_code8=demo_script_code8,chart_code8=chart_code8
        )
    else:
        
        return render_template('home.html')
 


@app.route('/aboutus',methods=['GET','POST'])
def aboutus():
    if(request.method=='POST'):
        return render_template('aboutus.html')
    else:
        return render_template('aboutus.html')


@app.route('/sectorwisecomp',methods=['GET','POST'])
def sectorwisecomp():
    allname=[]

    if(request.method=='POST'):
        f=request.files['file2']
        s=request.form['sector']
        df=pd.read_csv(f)
        allname=df.symbol.unique()
        
        f1=gold_comp(df,s)
        demo_script_code1,chart_code1=components(f1)
        return render_template('sectorwisecomp.html',demo_script_code1=demo_script_code1,chart_code1=chart_code1,allname=allname)
    else:
        # df=pd.read_excel('ALL DATA (1).xlsx')
        

        
        
        return render_template('sectorwisecomp.html',allname=allname)





@app.route('/hotstocks',methods=['GET','POST'])
def hotstocks():
    b,l=best()
    demo_script_code3,chart_code3=components(b)
    

    return render_template('hotstocks.html',demo_script_code3=demo_script_code3,chart_code3=chart_code3)



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)