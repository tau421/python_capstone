"""Models for favorite orders app."""

import os
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user
from wtforms.validators import DataRequired, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(3,19)])
    password = StringField(label='Password', validators=[Length(3,19)])
    submit = SubmitField(label='Submit')

class RestaurantForm(FlaskForm):
    restaurant_name = StringField(label = "Restaurant Name")
    menu_link = StringField(label = "Menu URL")
    restaurant_image = StringField(label = "Image URL")
    submit = SubmitField(label = "Submit")

class OrderForm(FlaskForm):
    text = StringField(label = "Order")
    submit = SubmitField(label = "Submit")

class User(db.Model, UserMixin):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    """Classmethods"""
    @classmethod
    def create_user(cls, username, password):
        """Create and return a new user."""

        return cls(username=username, password=password)
    
    @classmethod
    def get_user_by_id(cls, user_id):
        """Return user from id."""

        return cls.query.get(user_id)
    
    @classmethod
    def get_user_by_username(cls, username):
        """Return user from username."""

        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
    def get_restaurants_by_user_id(self):
        """Return user's restaurants."""

        return Restaurant.query.filter_by(user_id = self.user_id).all

    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'

class Restaurant(db.Model):
    """A restaurant."""

    __tablename__ = "restaurants"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_name = db.Column(db.String)
    menu_link = db.Column(db.String, nullable=True)
    restaurant_image = db.Column(db.String, nullable=True)
    is_favorite = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    user = db.relationship("User", backref="restaurants")

    """Classmethods."""
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def __repr__(self):
        return f'<Restaurant id={self.id} restaurant_name={self.restaurant_name}>'

class Order(db.Model):
    """An order."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurant.id))

    restaurant = db.relationship("Restaurant", backref="orders")

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def __repr__(self):
        return f'<Order id={self.id} text={self.text}>'

db.create_all()

def connect_to_db(flask_app, echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to db.")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)