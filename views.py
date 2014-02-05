from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User, Trip, PackListItems, Item, ActivityItem, Activity, TripActivity
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flaskext.markdown import Markdown
import config
import forms
import model
from datetime import date

app = Flask(__name__)
app.config.from_object(config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

Markdown(app)

### Routes ###

@app.route("/")
def index():
    if current_user.is_authenticated():
        trips = Trip.query.filter_by(user_id=current_user.id)
        return render_template("index.html", trips=trips)
    else:
        return render_template("landing.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
	form = forms.LoginForm(request.form)
	if not form.validate():
		flash("Incorrect username and/or password")
		return render_template("login.html")

	email = form.email.data
	password = form.password.data

	user = User.query.filter_by(email=email).first()

	if not user or not user.authenticate(password):
      	flash("Incorrect username and/or password") 
      	return render_template("login.html")

	login_user(user)
	return redirect(request.args.get("next", url_for("index")))

@app.route("/signup")
def register():
	return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def create_user():
	form = forms.RegisterForm(request.form)

	if not form.validate():
      	flash("All fields must be filled!")
      	return render_template("signup.html")

	first_name=form.first_name.data
	last_name=form.last_name.data
	email=form.email.data
	password=form.password.data

	existing = User.query.filter_by(email=email).first()
	if existing:
      	flash("Email is already registered!")
	else:
      	user = User(email=email, first_name=first_name, last_name=last_name, password=password, salt="random")
      	user.set_password(password)

      	model.session.add(user)
      	model.session.commit()
      	login_user(user)

	return url_for("index")

@app.route("/about"):
def about():
	return render_template("about.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")



@app.route("/new_trip", methods=["POST"])
@login_required
def create_trip():
	form = forms.NewTripForm(request.form)
	if not form.validate():
		flash("Error, all fields are required.")
	else:
		start_date = form.start_date.data.datetime.strftime('%d-%m-%Y')
		end_date = form.end_date.data.datetime.strptime('%d-%m-%Y')
		days_delta = end_date - start_date
		total_days = days_delta.days + 1

		trip = Trip(title=form.title.data, destination=form.destination.data, start_date=start_date, end_date=end_date, total_days=total_days)
		model.session.add(trip)
		model.session.commit()
		model.session.refresh(trip)

	return redirect(url_for("view_packinglist", id=trip.id))

@app.route("/trip/<int:id>")
@login_required
def view_trip(id):
	trip = Trip.query.get(id)
	packing_list = PackingList.query.filter_by(trip_id=trip.id).first()
	pack_items_list = PackListItems.query.filter_by(packing_list_id=packing_list.id).all()
	activity_list = TripActivity.query.filter_by(trip_id=trip.id).all()

	return render_template("trip.html", trip=trip, packing_list=packing_list, pack_items_list=pack_items_list, activity_list=activity_list)


@app.route("/trip/<int:id>")
@login_required
def view_packinglist(id):
	trip = Trip.query.get(id)
	return render_template("trip.html", trip = trip)








@app.route("/settings")
@login_required
def settings():
	return render_template("settings.html")





@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

