"""Server for favorite orders app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from model import connect_to_db, db, User, Restaurant, Order, LoginForm

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev_mtn_capstone"
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("home.html", form=LoginForm())

@app.route("/restaurants")
@login_required
def all_users():
    """View all users."""

    restaurants = Restaurant.get_all_restaurants

    return render_template("restaurants.html", restaurants=restaurants)

@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html", form=LoginForm())

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", form=LoginForm())

@app.route("/signup", methods=["POST"])
def signup_user():
    print(request.form)
    user = User(username = request.form["username"], password = request.form["password"])
    if user:
        flash("Can't create an account with that username.  Please try again.")
    else:
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created.  Please log in.")
        
    return redirect("/")

@app.route("/login", methods=["POST"])
def handle_login():
    print(request.form)
    user = User.query.filter_by(username = request.form["username"], password = request.form["password"]).first()
    if user is not None:
        login_user(user)
        return redirect("/restaurants")
    else:
        flash("Wrong username or password.")
        return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details for a specific user."""

    user = User.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

### Need to add restaurant and orders ###

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)