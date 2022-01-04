from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Session Setup
app.secret_key = "csuglobal"
app.permanent_session_lifetime = timedelta(days=1)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# class Entity(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     created_at = db.Column(DateTime)
#     updated_at = db.Column(DateTime)
#     last_updated_by = db.Column(db.String)
#
#     def __init__(self, created_by):
#         self.created_at = datetime.now()
#         self.updated_at = datetime.now()
#         self.last_updated_by = created_by


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    # Create Session
    if request.method == "POST":
        name = request.form["nm"]
        session["user"] = name
        # Get User from DB
        found_user = users.query.filter_by(name=name).first()
        if found_user:
            session["email"] = found_user.email
        else:
            # Add user to DB
            usr = users(name, "")
            db.session.add(usr)
            db.session.commit()
        flash("Login successful")
        return redirect(url_for("user"))
    else:
        # If already logged in send to user page
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Clear Session Variables
    if "user" in session:
        user_name = session["user"]
        flash(f"{user_name} successfully logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/user", methods=["POST", "GET"])
def user():
    # Get session or send to login screen
    email = None
    if "user" in session:
        user_name = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            # Get User from DB
            found_user = users.query.filter_by(name=user_name).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/view_users")
def view_users():
    return render_template("view_users.html", values=users.query.all())

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
