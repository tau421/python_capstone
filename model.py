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

    """Classmethods"""
    @classmethod
    def create_user(cls, username, password):
        """Create and return a new user."""

        return cls(user=username, password=password)
    
    @classmethod
    def get_user_by_id(cls, user_id):
        """Return user from id."""

        return cls.query.get(user_id)
    
    @classmethod
    def get_user_by_username(cls, username):
        """Return user from username."""

        return cls.query.filter(User.username == username).first()
    
    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
    # def get_restaurants_by_user_id(user_id):
    #     """Return user's restaurants."""

    #     return Restaurant.query.get(user_id)

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

    """Classmethods."""
    @classmethod
    def create_restaurant(cls, user, restaurant_name, menu_link, restaurant_image, is_favorite):
        """Create and return a new restaurant."""

        return cls(user=user, restaurant_name=restaurant_name, menu_link=menu_link, restaurant_image=restaurant_image, is_favorite=is_favorite)

    @classmethod
    def get_all_restaurants(cls):
        """Return all restaurants."""

        return cls.query.all()
    
    @classmethod
    def get_restaurant_by_restaurant_id(cls, restaurant_id):
        """Return a restaurant by restaurant id."""

        return cls.query.get(restaurant_id)

    # def get_orders_by_restaurant_id(restaurant_id):
    #     """Return orders from specific restaurant."""

    #     return Order.query.get(restaurant_id)

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
 
    """Classmethods."""
    @classmethod
    def create_order(cls, restaurant, order_description):
        """Create and return a new order."""

        return cls(restaurant=restaurant, order_description=order_description)
    
    @classmethod
    def update_order(cls, order_id, new_description):
        """Update an order given order_id and updated order."""

        order = cls.query.get(order_id)
        order.order_description = new_description

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