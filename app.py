from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

app = Flask(__name__)
# Session Setup
app.secret_key = "csuglobal"
app.permanent_session_lifetime = timedelta(days=1)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    address = db.Column("address", db.String(100))
    phone = db.Column("phone", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


class pothole_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column("street_address", db.String(100))
    size = db.Column("size", db.Integer)
    priority = db.Column("priority", db.Integer)
    location = db.Column("location", db.String(100))
    damage_type = db.Column("damage_type", db.String(100))
    user = db.Column("user", db.String(100))

    def __init__(self, street_address, location, damage_type, size):
        self.street_address = street_address
        self.location = location
        self.damage_type = damage_type
        self.size = size
        self.priority = int(size) * 2
        if "user" in session:
            user_name = session["user"]
        self.user = user_name


class work_order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer)
    equipment = db.Column("equipment", db.String(100))
    crew = db.Column("repair_crew", db.String(100))
    hours = db.Column("hours", db.Integer)
    filler = db.Column("filler", db.Integer)
    cost = db.Column("cost", db.Integer)

    def __init__(self, report_id, equipment, crew, hours, filler):
        self.report_id = report_id
        self.equipment = equipment
        self.crew = crew
        self.hours = hours
        self.filler = filler
        self.cost = (int(hours) * int(crew)) + (int(filler) * 2)


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
            address = request.form["address"]
            phone = request.form["phone"]
            session["email"] = email
            # Get User from DB
            found_user = users.query.filter_by(name=user_name).first()
            found_user.email = email
            found_user.address = address
            found_user.phone = phone
            db.session.commit()
            flash("Info was saved")
        else:
            if "email" in session:
                email = session["email"]
                found_user = users.query.filter_by(name=user_name).first()
                address = found_user.address
                phone = found_user.phone
        return render_template("user.html", email=email, address=address, phone=phone)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route("/view_users")
def view_users():
    return render_template("view_users.html", values=users.query.all())


@app.route("/report_pothole", methods=["POST", "GET"])
def new_report():
    if request.method == "POST":
        address = request.form["address"]
        location = request.form["location"]
        damage_type = request.form["damage_type"]
        size = request.form["size"]
        report = pothole_report(address, location, damage_type, size)
        db.session.add(report)
        db.session.commit()
        flash("Report Created")
        return render_template("report_pothole.html")

    else:
        return render_template("report_pothole.html")


@app.route("/view_pothole")
def view_pothole_report():
    return render_template("view_pothole_report.html", values=pothole_report.query.all())


@app.route("/create_workorder/<report_id>", methods=["POST", "GET"])
def create_workorder(report_id):
    if request.method == "POST":
        global message
        equipment = request.form["equipment"]
        crew = request.form["crew"]
        hours = request.form["hours"]
        filler = request.form["filler"]
        new_workorder = work_order(report_id, equipment, crew, hours, filler)
        db.session.add(new_workorder)
        db.session.commit()
        flash("WorkOrder Created")
        return view_pothole_report()
    else:
        report = pothole_report.query.filter_by(id=report_id).first()
        return render_template("create_workorder.html", id=report_id, street_address=report.street_address)

@app.route('/view_workorders')
def view_workorder():
    return render_template("view_workorders.html", values=work_order.query.all())


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
