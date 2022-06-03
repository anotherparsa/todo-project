from flask import Flask, redirect, render_template, request
import mysql.connector

app = Flask(__name__)

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
    return render_template("home/home.html")

#registration part:
#registraiton page:
@app.route("/registration")
def registration():
    return render_template("registration/registration.html")

#registration operation
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if len(username) <= 10 and len(password) <= 12:
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
            return redirect("/")
    else:
        return "your information doesn't have the requeirenments"


#loign part:
#login page:
@app.route("/login")
def login():
    return render_template("login/login.html")

#logging in operation
@app.route("/log", methods=["POST"])
def log():
    username = request.form.get("username")
    password = request.form.get("password")
    if len(username) <= 10 and len(password) <= 12:
        mycursor.execute("use users")
        mycursor.execute(f"SELECT * FROM user WHERE username='\{username}\' AND password='\{password}\' ")
        userValid = mycursor.fetchall()
        if userValid:
            return redirect("/")
        else:
            return "your information isn't correct"
    else:
        return "OOps something went wrong"







if __name__ == "__main__":
    app.run(debug=True)
