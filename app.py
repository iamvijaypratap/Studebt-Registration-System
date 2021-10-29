from flask import Flask,redirect,url_for,render_template,request,g
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import flash
from flask.globals import session
import pymysql
pymysql.install_as_MySQLdb()

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
app.secret_key = 'super secret key'

class Tbl_student(db.Model):
    sno=db.Column(db.Integer,primary_key = True)
    Name=db.Column(db.String(50),nullable = False)
    College_Name = db.Column(db.String(100),nullable = False)
    Specialistion = db.Column(db.String(100),nullable = False)
    Degree_Name = db.Column(db.String(100),nullable = False)
    Applied_for = db.Column(db.String(100),nullable = False)
    phone =db.Column(db.Integer,nullable = False)
    emailid = db.Column(db.String(100),nullable = False)	
    location = db.Column(db.String(100),nullable=False)
    Gender = db.Column(db.String(100),nullable=False)
    notes = db.Column(db.String(100),nullable=False)

class Admin_Signup(db.Model):
    sno=db.Column(db.Integer,primary_key = True)
    Name=db.Column(db.String(50),nullable = False)
    Username=db.Column(db.String(50),nullable = False)
    Email = db.Column(db.String(100),nullable = False)
    Password= db.Column(db.String(100),nullable = False)

db.create_all()

@app.route('/Admin_Signup', methods=['GET', 'POST'])
def Signup():
     if request.method=="POST":
        Name=request.form.get("name")
        username = request.form.get("username")
        Password =request.form.get("password")
        Confirmpassword = request.form.get("confirmpassword")
        Email = request.form.get("email")
        if Admin_Signup.query.filter_by(Username=username).first():
            flash("Username already exists","danger")
        elif len(Password) <8: 
            flash("Password too Short","danger")
        elif Admin_Signup.query.filter_by(Email=Email).first():
            flash("Email already Exists","danger")
        if Password==Confirmpassword:
            EntryToDatabase = Admin_Signup(Name=Name,
            Email=Email,Username=username,
            Password=Password) 
            db.session.add (EntryToDatabase)
            db.session.commit()
            flash("Account Created Successfully Now You Can Log in","success")
            return redirect("login")
        else:
            flash("Password did not match !","danger")
     return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def Admin_Log_In():
    if g.user:
        return redirect("/show")
    if request.method=="POST":
        user=request.form.get("username")
        passw = request.form.get("password")
        validateData = Admin_Signup.query.filter_by(Username=user).first()
        if validateData is not None:
            if user==validateData.Username and passw==validateData.Password:
                session['user'] = user
                return redirect("/show")
        else:
            flash("Invalid Credentials","danger")
    return render_template("admin.html")
@app.route('/logout', methods=['GET', 'POST'])
def Logout():
    session.pop("user")
    flash("Your Logged Out","danger")
    return redirect("/login")
@app.before_request
def before_request():
    g.user=None
    if "user" in session:
        g.user=session["user"]

@app.route('/',methods=["GET","POST"])
def AddData():
     if request.method=="POST":
        Name = request.form.get("name")
        College_name = request.form.get("college")
        Specialistion = request.form.get("specialistion")
        Degree_Name= request.form.get("degree")
        Applied_For = request.form.get("internship")
        phone= request.form.get("phone")
        emailid = request.form.get("email")
        location = request.form.get("location")
        gender = request.form.get("gender")
        notes = request.form.get("notes")
        Entry = Tbl_student(Name=Name,College_Name=College_name,Specialistion=Specialistion,Degree_Name=Degree_Name,Applied_for=Applied_For
        ,phone=phone,emailid=emailid,location=location,Gender=gender,notes=notes)
        db.session.add(Entry)
        db.session.commit()
        flash("Your Registration form has been Submitted","success")
        return render_template("confirmationpage.html")
     return render_template("home.html")
@app.route('/delete/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    if g.user:
        alldata=Tbl_student.query.filter_by(sno=sno).first()
        db.session.delete(alldata)
        db.session.commit()
        return redirect("/show")
    else:
        return redirect("/login")
@app.route('/show')
def ShowData():
    if g.user:
        alldata=Tbl_student.query.all()
        return render_template("data.html",alldata=alldata)
    else:
        return redirect("/login")



if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)