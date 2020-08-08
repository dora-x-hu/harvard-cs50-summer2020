import os
import datetime
import time
import pytz

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///planner.db")

@app.route("/")
@login_required
def tasks():

    """ show lists of all tasks this user has added so far """

    current_user = session["user_id"]

    tasks = db.execute("SELECT * FROM tasks WHERE user_id=:user AND completed=0 ORDER BY date, start, end", user=current_user)

    if len(tasks) == 0:
        return render_template("tasks.html", tasks=tasks)

    return render_template("tasks.html", tasks=tasks)


@app.route("/login", methods=["GET", "POST"])
def login():

    """ log in user """

    session.clear()

    # user is submitting login info
    if request.method=="POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("sorry.html", query="valid username and password", method="login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # user is getting to the login page
    else:

        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():

    """ log out user """

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():

    """ register a new user """

    if request.method=="POST":


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username is not already taken
        if len(rows) == 1:
            return render_template("sorry.html", query="username that hasn't been taken yet", method="register")

        # Ensure that the passwords match
        if request.form["password"] != request.form["confirmation"]:
            return render_template("sorry.html", query="confirmation that matches your password", method="register")

        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))


        # Redirect user to home page
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    """ add tasks to task list """

    if request.method=="POST":

        # Ensure that the start time is before the end time
        if request.form["startTime"] > request.form["endTime"]:
            return render_template("sorry.html", query="start time that comes before the end time", method="add")

        # Ensure that (the day of the task hasn't passed already) and (if the day is today, the end time hasn't passed already)


        tag = request.form.get("tag")

        description = request.form["description"]
        user_id = session["user_id"]


        date = request.form["date"]
        start = request.form["startTime"]
        end = request.form["endTime"]


        #start = datetime.datetime(date.year, date.month, date.day, startTime.hour, startTime.minute, startTime.second)
        #end = datetime.datetime(date.year, date.month, date.day, endTime.hour, endTime.minute, endTime.second)



        db.execute("INSERT INTO tasks (tag, description, completed, user_id, start, end, date) VALUES(:tag, :description, 0, :user_id, :start, :end, :date);", tag=tag, description=description, user_id=user_id, start=start, end=end, date=date)

        return redirect("/")

    else:

        tags = ["Work", "Study", "Chores", "Social", "Rest", "Entertainment"]

        return render_template("add.html", tags=tags)


@app.route("/delete", methods=["POST"])
@login_required
def delete():

    confirmed = request.form["confirmed"]

    if confirmed=="true":
        db.execute("DELETE FROM tasks WHERE task_id=:task_id", task_id=request.form["thistask"])

    return redirect("/")

@app.route("/confirmdelete", methods=["POST"])
@login_required
def confirmdelete():

    task = db.execute("SELECT * FROM tasks WHERE task_id=:task_id", task_id=request.form["thistask"])

    return render_template("delete.html", tasks=task)




@app.route("/complete", methods=["POST"])
@login_required
def complete():

    confirmed = request.form["confirmed"]

    if confirmed=="true":
        db.execute("UPDATE tasks SET completed=1 WHERE task_id=:task_id", task_id=request.form["thistask"])

    return redirect("/")


@app.route("/confirmcomplete", methods=["POST"])
@login_required
def confirmcomplete():

    task = db.execute("SELECT * FROM tasks WHERE task_id=:task_id", task_id=request.form["thistask"])

    return render_template("complete.html", tasks=task)



@app.route("/retrieve", methods=["POST"])
@login_required
def retrieve():

    confirmed = request.form["confirmed"]

    if confirmed=="true":
        db.execute("UPDATE tasks SET completed=0 WHERE task_id=:task_id", task_id=request.form["thistask"])

    return redirect("/")

@app.route("/confirmretrieve", methods=["POST"])
@login_required
def confirmretrieve():

    task = db.execute("SELECT * FROM tasks WHERE task_id=:task_id", task_id=request.form["thistask"])

    return render_template("retrieve.html", tasks=task)


@app.route("/editpage", methods=["POST"])
@login_required
def editpage():

    tasks = db.execute("SELECT * FROM tasks WHERE task_id=:task_id", task_id=request.form["thistask"])

    tags = ["Work", "Study", "Chores", "Social", "Rest", "Entertainment"]

    return render_template("edit.html", task=tasks[0], tags=tags)

@app.route("/edit", methods=["POST"])
@login_required
def edit():

    # Ensure that the start time is before the end time
        # Ensure that the start time is before the end time
        if request.form["startTime"] > request.form["endTime"]:
            return render_template("sorry.html", query="start time that comes before the end time", method="edit")

        # Ensure that (the day of the task hasn't passed already) and (if the day is today, the end time hasn't passed already)


        tag = request.form.get("tag")

        description = request.form["description"]


        date = request.form["date"]
        start = request.form["startTime"]
        end = request.form["endTime"]

        task_id = request.form["thistask"]

        db.execute("UPDATE tasks SET tag=:tag, description=:description, date=:date, start=:start, end=:end WHERE task_id=:task_id", tag=tag, description=description, date=date, start=start, end=end, task_id=task_id)

        return redirect("/")

@app.route("/history", methods=["GET"])
@login_required
def history():

    current_user = session["user_id"]

    tasks = db.execute("SELECT * FROM tasks WHERE user_id=:user AND completed=1 ORDER BY date DESC, start DESC, end DESC", user=current_user)

    return render_template("taskhistory.html", tasks=tasks)