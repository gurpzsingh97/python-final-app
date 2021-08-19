import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bookings")
def bookings():
    bookings = list(mongo.db.bookings.find())
    return render_template("bookings.html", bookings=bookings)


@app.route("/create_booking")
def create_booking():
    return render_template("create_booking.html")


@app.route("/houses")
def houses():
    return render_template("houses.html")


@app.route("/house1")
def house1():
    return render_template("house1.html")


@app.route("/house2")
def house2():
    return render_template("house2.html")


@app.route("/house3")
def house3():
    return render_template("house3.html")


@app.route("/login_warning")
def login_warning():
    flash("Log In or Register to make bookings")
    return render_template("login.html")



@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("{}, you're in!!!!" .format(
                        request.form.get("username")))
                    return redirect((url_for(
                        "index", username=session["user"])))
            else:
                flash("Incorrect Username or Password")
                return redirect(url_for("login"))
        else:
            flash("Username or Password is incorrect")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("username already exists")
            return redirect(url_for("register"))
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)
        session["user"] = request.form.get("username").lower()
        flash("Registration succesful!!")
        return redirect((url_for("index", username=session["user"])))
    return render_template("register.html")


@app.route("/logout")
def logout():
    flash("You've been logged out succesfully")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP",),
        port=int(os.environ.get("PORT")),
        debug=True)
    
