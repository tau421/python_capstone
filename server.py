"""Server for favorite orders app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db, db, User, Restaurant, Order

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev_mtn_capstone"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/users")
def all_users():
    """View all users."""

    users = User.get_all_users()

    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.get_user_by_username(username)
    if user:
        flash("Cannot create an acocunt with that username.  Please try again.")
    else:
        user = User.create_user(username, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!  Please log in.")

    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details for a specific user."""

    user = User.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    username = request.form.get("username")
    password = password.request.get("password")

    user = User.get_user_by_username(username)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_username"] = user.username
        flash(f"Welcome back, {user.username}!")
    
    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)