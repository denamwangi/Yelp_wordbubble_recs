

"""This file will read in the various json files that are provided a part of the
Yelp Data Challenge. It will create Classes for the data model used for the
project."""


#There will be 7 tables with two of them borne from the business tables

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.secret_key = "ABC"

db = SQLAlchemy()


##############################################################################
# Model definitions

class Business(db.Model):
    """Business profile data."""

    __tablename__ = "businesses"

    business_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    neighborhood = db.Column(db.String)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    stars = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    is_open = db.Column(db.Boolean)
    # attributes = db.Column(db.PickleType)    # Array of attributes like parking, cash only etc
    attr_check = db.Column(db.PickleType)    # Array- need this unpacked

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Business name=%s stars=%s >" % (self.name,
                                                 self.reviews)


class User(db.Model):
    """User data."""

    __tablename__ = "users"

    user_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)             # first name
    review_count = db.Column(db.Integer)
    yelping_since = db.Column(db.DateTime)
    friends = db.Column(db.PickleType)                          # PickleType of friend encrypted id's
    useful = db.Column(db.Integer)
    funny = db.Column(db.Integer)
    cool = db.Column(db.Integer)
    fans = db.Column(db.Integer)
    elite = db.Column(db.PickleType)                            # PickleType of years as elite
    average_stars = db.Column(db.Float)
    compliment_hot = db.Column(db.Integer)
    compliment_more = db.Column(db.Integer)
    compliment_profile = db.Column(db.Integer)
    compliment_cute = db.Column(db.Integer)
    compliment_list = db.Column(db.Integer)
    compliment_note = db.Column(db.Integer)
    compliment_plain = db.Column(db.Integer)
    compliment_cool = db.Column(db.Integer)
    compliment_funny = db.Column(db.Integer)
    compliment_writer = db.Column(db.Integer)
    compliment_photos = db.Column(db.Integer)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User name=%s reviews=%s >" % (self.name,
                                               self.reviews)


class Tip(db.Model):
    """Tips (Mini/short snippet reviews of an establishment. """

    __tablename__ = "tips"

    tip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    business_id = db.Column(db.String, db.ForeignKey('businesses.business_id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.user_id'), nullable=False)
    
    business = db.relationship('Business', backref=db.backref('tips', order_by=date))
    user = db.relationship('User', backref=db.backref('tips', order_by=date))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Tip business_id=%s likes=%s >" % (self.business_id,
                                                   self.likes)


class Review(db.Model):
    """Reviews and Ratings of each establishment."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.user_id'), nullable=False)
    business_id = db.Column(db.String, db.ForeignKey('businesses.business_id'), nullable=False)
    stars = db.Column(db.Float)
    date = db.Column(db.DateTime)
    text = db.Column(db.String, nullable=False)
    useful = db.Column(db.Integer)
    funny = db.Column(db.Integer)
    cool = db.Column(db.Integer)
    
    business = db.relationship('Business', backref=db.backref('reviews', order_by=date))
    user = db.relationship('User', backref=db.backref('reviews', order_by=date))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Review stars=%s useful=%s >" % (self.stars,
                                                 self.useful)


class Category(db.Model):
    """Categories - each business can have multiple. Pulling from business json"""

    __tablename__ = "categories"

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String, db.ForeignKey('businesses.business_id'), nullable=False)  # foreignkey
    category = db.Column(db.String, nullable=False)

    business = db.relationship('Business', backref=db.backref('categories'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category business_id=%s likes=%s >" % (self.business_id,
                                                        self.category)


class Attribute(db.Model):
    """Attributes - each business can have multiple or none. Pulling from business json"""

    __tablename__ = "attributes"

    attr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String, db.ForeignKey('businesses.business_id'), nullable=False)  # foreignkey
    attribute_key = db.Column(db.String, nullable=False)
    attribute_value = db.Column(db.String, nullable=False)

    business = db.relationship('Business', backref=db.backref('attributes'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Attribute attr_id=%s attribute=%s >" % (self.business_id,
                                                         self.attribute)





##############################################################################
# Helper functions

# def init_app():
#     # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
#     from flask import Flask
#     app = Flask(__name__)

#     connect_to_db(app)
#     print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///yelp'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

# from flask import Flask
# app = Flask(__name__)
if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    

    connect_to_db(app)
    print "Connected to DB."

