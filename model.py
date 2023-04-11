"""Models for favorite orders app."""

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'
    
class Restaurant(db.Model):
    """A restaurant."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_name = db.Column(db.String)
    menu_link = db.Column(db.String, nullable=True)
    restaurant_image = db.Column(db.String, nullable=True)
    is_favorite = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="restaurants")

    def __repr__(self):
        return f'<Restaurant restaurant_id={self.restaurant_id} restaurant_name={self.restaurant_name}>'

class Order(db.Model):
    """An order."""

    __tablename__ = "orders"

    order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    order_description = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"))

    restaurant = db.relationship("Restaurant", backref="orders")

    def __repr__(self):
        return f'<Order order_id={self.order_id} order_description={self.order_description}>'
 
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