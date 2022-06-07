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

#home route
@app.route("/")
def home():
    if session.get("username") == "Admin":
        return redirect("/admin")

    elif session.get("username"):
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

#registration operation:
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

#logging in operation:
@app.route("/log", methods=["POST"])
def log():
    username = request.form.get("username")
    password = hashlib.sha256(request.form.get("password").encode("utf-8")).hexdigest()
    mycursor.execute("use users")
    mycursor.execute(f"SELECT username FROM user WHERE username='\{username}\' AND password='\{password}\' ")
    userValid = mycursor.fetchall()
    if userValid:
        session["username"] = username
        session.permanent = True
        return redirect("/")
    else:
        return "your information isn't correct"


#logging out:
@app.route("/logout")
def logout():
    session["username"] = ""
    return redirect("/")

#submitting the task to store in database:
@app.route("/submittask", methods=["POST"])
def submitTask():
    isdone = "0"
    owner = session.get("username")
    priority = request.form.get("priority")
    task = request.form.get("task")
    mycursor.execute("use users")
    mycursor.execute(f"INSERT INTO task (task, priority, isdone, owner) VALUES (\'{task}\',\'{priority}\',\'{isdone}\',\'{owner}\')")
    db.commit()
    return redirect("/")

#deleting the task from database:
@app.route("/deletetask/<owner>/<int:keyfordel>")
def deletetask(owner, keyfordel):
    if owner != session.get("username"):
        return "sorry you're not authorized for this"
    else:
        mycursor.execute("use users")
        mycursor.execute(f"DELETE FROM task WHERE id={keyfordel} AND owner=\'{owner}\' ")
        db.commit()
        return redirect("/")

#done and un-done part:
@app.route("/isdone/<owner>/<int:key>/<int:status>")
def isdone(owner, key, status):
    if owner != session.get("username"):
        return "sorry you're not authorized for this"
    else:
        mycursor.execute("use users")
        if status == 1:
            mycursor.execute(f"UPDATE task SET isdone='0' WHERE id=\'{key}\' AND owner=\'{owner}\'")
            db.commit()
            return redirect("/")
        elif status == 0:
            mycursor.execute(f"UPDATE task SET isdone='1' WHERE id=\'{key}\' AND owner=\'{owner}\'")
            db.commit()
            return redirect("/")
        else:
            return "something went wrong"

#editing the task:
@app.route("/edittask/<owner>/<int:keyforedit>/<task>")
def edittask(owner, task, keyforedit):
    if owner != session.get("username"):
        return "sorry you're not authorized for this"
    else:
        return render_template("edit/edit.html", task=task, owner=owner, keyforedit=keyforedit)
    
@app.route("/updatetask/<owner>/<int:keyforedit>", methods=["post"])
def updatetask(owner, keyforedit):
    if owner != session.get("username"):
        return "sorry you're not authorized for this"
    else:
        newTask = request.form.get("updated")
        mycursor.execute("use users")
        mycursor.execute(f"UPDATE task SET task=\'{newTask}\' WHERE id=\'{keyforedit}\' AND owner=\'{owner}\' ")
        db.commit()
        return redirect("/")

#deleting account part
@app.route("/deleteaccount/<userDelete>")
def userdelete(userDelete):
    if session.get("username") == userDelete:   
        mycursor.execute("use users")
        mycursor.execute(f"DELETE FROM user WHERE username=\'{userDelete}\'")
        mycursor.execute(f"DELETE FROM task WHERE owner=\'{userDelete}\'")
        db.commit()
        return redirect("/registration")
    else:
        return "sorry you're not authorized for this"

#404 page
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404/404.html"), 404

#changing user pass:
@app.route("/changepassword/<user>")
def changepassword(user):
    if user != session.get("username"):
        return "sorry you're not authorized for this"
    else:
        return render_template("changepass/changepass.html", user=user)
    
@app.route("/cpass/<user>", methods=["post"])
def updatetas3k(user):
    if user != session.get("username"):
        return "sorry you're not authorized for this"
    else:
        newpass = hashlib.sha256(request.form.get("newpassword").encode("utf-8")).hexdigest()
        mycursor.execute("use users")
        mycursor.execute(f"UPDATE user SET password=\'{newpass}\' WHERE username=\'{user}\' ")
        db.commit()
        return redirect("/")

#admin page
@app.route("/admin")
def admin():
    mycursor.execute("use users")
    mycursor.execute(f"SELECT username FROM user WHERE username='Admin' AND rule='admin' ")
    isThisAdmin = mycursor.fetchall()
    if session.get("username") == "Admin" and isThisAdmin:
        mycursor.execute("use users")
        mycursor.execute("SELECT username FROM user")
        totalAccount = len(mycursor.fetchall())
        mycursor.execute("SELECT task FROM task")
        totalTask = len(mycursor.fetchall())
        return render_template("admin/admin.html", totalAccount=totalAccount, totalTask=totalTask )

        


if __name__ == "__main__":
    app.run(debug=True)
