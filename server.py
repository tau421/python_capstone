"""Server for favorite orders app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from model import connect_to_db, db, User, Restaurant, Order, LoginForm, RestaurantForm, OrderForm

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

@app.route("/restaurants", methods=["GET", "POST"])
@login_required
def all_restaurants():
    """View user's restaurants."""

    if request.method == "GET":
        return render_template("restaurants.html", restaurants = Restaurant.query.filter_by(user_id = current_user.id), form=RestaurantForm())
    else:
        r = Restaurant(restaurant_name = request.form["restaurant_name"], menu_link = request.form["menu_link"], restaurant_image = request.form["restaurant_image"], user_id = current_user.id)
        db.session.add(r)
        db.session.commit()
        return redirect("/restaurants")

@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html", form=LoginForm())

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", form=LoginForm())

@app.route("/signup", methods=["POST"])
def signup_user():
    print(request.form)
    existing_user = User.query.filter_by(username = request.form["username"]).first()
    if existing_user is None:
        user = User(username = request.form["username"], password = request.form["password"])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created.  Please log in.")
        return redirect("/login")
    else:
        flash("Can't create an account with that username.  Please try again.")
        return redirect("/signup")

@app.route("/login", methods=["POST"])
def handle_login():
    print(request.form)
    user = User.query.filter_by(username = request.form["username"], password = request.form["password"]).first()
    if user is not None:
        login_user(user)
        flash(f'Welcome back {user.username}!')
        return redirect("/restaurants")
    else:
        flash("Wrong username or password.")
        return redirect("/login")

@app.route("/logout")
@login_required
def logout():
    logout_user
    flash("You are now logged out.")
    return redirect("/")

@app.route("/restaurants/<id>", methods=["GET"])
@login_required
def show_orders(id):
    """Show orders for a particular restaurant."""

    restaurant = Restaurant.get_by_id(id)
    orders = Order.query.filter_by(restaurant_id = id).all()
    return render_template("/restaurant_orders.html", restaurant=restaurant, orders=orders, form = OrderForm())

@app.route("/restaurants/<id>/orders", methods=["POST"])
@login_required
def create_order(id):
    """Create a new order for the restaurant."""

    restaurant = Restaurant.get_by_id(id)
    o = Order(text = request.form["text"], restaurant=restaurant)
    db.session.add(o)
    db.session.commit()
    return redirect(f"/restaurants/{id}")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)