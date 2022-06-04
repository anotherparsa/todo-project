from flask import Flask, redirect, render_template, request, session
import mysql.connector
import hashlib

app = Flask(__name__)

app.secret_key = "7h151553cr37k3y7h47n0b0dy5h0uldkn0w"
#connecting to database:
db = mysql.connector.connect(
    host = "IP",
    user = "USERNAME",
    password = "PASSWORD"
)

#defining cursor:
mycursor = db.cursor()

@app.route("/")
def home():
    if session.get("username"):
        owner = session.get("username")
        mycursor.execute("use users")
        mycursor.execute(f"SELECT * FROM task WHERE owner=\'{owner}\' ")
        tasks = mycursor.fetchall()
        tasknumber = len(tasks)
        return render_template("home/home.html", user=owner, tasks=tasks, tasknumber=tasknumber)
    else:
        return redirect("/login")
    

#registration part:
#registraiton page:
@app.route("/registration")
def registration():
    return render_template("registration/registration.html")

#registration operation
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = hashlib.sha256(request.form.get("password").encode("utf-8")).hexdigest()
    mycursor.execute("use users")
    mycursor.execute(f"SELECT * FROM user WHERE username='\{username}\' ")
    userExist = mycursor.fetchall()
    rule = "user"
    if userExist:
        return "sorry the username is already exist"
    else:
        mycursor.execute("use users")
        mycursor.execute(f"INSERT INTO user (username, password, rule) VALUES (\'{username}\', \'{password}\', \'{rule}\')")
        db.commit()
        session["username"] = username
        session.permanent = True
        return redirect("/")


#loign part:
#login page:
@app.route("/login")
def login():
    return render_template("login/login.html")

#logging in operation
@app.route("/log", methods=["POST"])
def log():
    username = request.form.get("username")
    password = hashlib.sha256(request.form.get("password").encode("utf-8")).hexdigest()
    mycursor.execute("use users")
    mycursor.execute(f"SELECT * FROM user WHERE username='\{username}\' AND password='\{password}\' ")
    userValid = mycursor.fetchall()
    if userValid:
        session["username"] = username
        session.permanent = True
        return redirect("/")
    else:
        return "your information isn't correct"


#logging out
@app.route("/logout")
def logout():
    session["username"] = ""
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
