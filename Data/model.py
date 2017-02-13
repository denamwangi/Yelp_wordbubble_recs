

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

    business_id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    neighborhood = db.Column(db.String)
    address = db.Column(db.String, nullable=False)
    
    postal_code = db.Column(db.String)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    stars = db.Column(db.Float, nullable=False)
    review_count = db.Column(db.Integer, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)

    categories = db.relationship('Category', secondary='business_category_location',
                                             backref='businesses')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Business name=%s stars=%s >" % (self.name,
                                                 self.reviews)


class Category(db.Model):
    """Categories master list- each business can have multiple.
        Pulling from Yelp page of all categories"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True)
    category = db.Column(db.String(120), primary_key=True, nullable=False)
    
    # locations = db.relationship('Location', secondary='business_category_place',
    #                                          backref='categories')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category=%s >" % (self.category_id,
                                                           self.category)


class Location(db.Model):
    """Location master list- pulling from the yelp list of cities for datachallenge 9"""

    __tablename__ = "locations"
    city = db.Column(db.String(120), primary_key=True)
    state = db.Column(db.String(10)),
    city_id = db.Column(db.String(20))

    businesses = db.relationship('Business', secondary='business_category_location',
                                             backref='locations')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Location category_id=%s category=%s >" % (self.city_id,
                                                           self.city)

class BusinessCategoryLocation(db.Model):
    """Association table linking the business category and place"""

    __tablename__ = "business_category_location"

    bcl_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String(120), 
                            db.ForeignKey('businesses.business_id'), 
                            nullable=False)  # foreignkey
    category = db.Column(db.String(120), db.ForeignKey('categories.category'), nullable=False)
    city = db.Column(db.String(120),
                     db.ForeignKey('locations.city'),
                     nullable=False)
    state = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<BusinessCategoryLocation business_id=%s category=%s >" % (self.business_id,
                                                           self.state)


class Keyword(db.Model):
    """Keywords master table - each business can have multiple. These will be as
        a result of some NLP analysis"""

    __tablename__ = "keywords"

    keyword_id = db.Column(db.String(15), primary_key=True)
    keyword = db.Column(db.String(120), nullable=False)

    businesses = db.relationship('Business', secondary='businesses_keywords',
                                             backref='keywords')
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Keyword keyword_id=%s keyword=%s >" % (self.keyword_id,
                                                         self.keyword)


class BusinessKeyword(db.Model):
    """Keywords and business association table  - each business can have multiple.
        These will be as a result of some NLP analysis"""

    __tablename__ = "businesses_keywords"

    buskey_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String(120), db.ForeignKey('businesses.business_id'), nullable=False)  # foreignkey
    keyword_id = db.Column(db.String(15), db.ForeignKey('keywords.keyword_id'), nullable=False)
    keyword_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<BusinessKeyword business_id=%s keyword=%s >" % (self.business_id,
                                                         self.keyword_count)


class User(db.Model):
    """User data."""

    __tablename__ = "users"

    user_id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(64), nullable=False)             # first name
    review_count = db.Column(db.Integer, nullable=False)
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
                                               self.review_count)


class Tip(db.Model):
    """Tips (Mini/short snippet reviews of an establishment. """

    __tablename__ = "tips"

    tip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    business_id = db.Column(db.String(120), db.ForeignKey('businesses.business_id'), nullable=False)
    user_id = db.Column(db.String(120), db.ForeignKey('users.user_id'), nullable=False)
    
    business = db.relationship('Business', backref=db.backref('tips', order_by=date))
    user = db.relationship('User', backref=db.backref('tips'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Tip business_id=%s likes=%s >" % (self.business_id,
                                                   self.likes)


class Review(db.Model):
    """Reviews and Ratings of each establishment."""

    __tablename__ = "reviews"

    review_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String(120), db.ForeignKey('users.user_id'), nullable=False)
    business_id = db.Column(db.String(120), db.ForeignKey('businesses.business_id'), nullable=False)
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


class Attribute(db.Model):
    """Attributes - each business can have multiple or none. Pulling from business json"""

    __tablename__ = "attributes"

    attr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String(120), db.ForeignKey('businesses.business_id'), nullable=False)  # foreignkey
    attribute_key = db.Column(db.String, nullable=False)
    attribute_value = db.Column(db.String, nullable=False)

    business = db.relationship('Business', backref=db.backref('attributes'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Attribute attr_id=%s attribute=%s : %s >" % (self.business_id,
                                                              self.attribute_key,
                                                              self.attribute_value)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///yelp'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    connect_to_db(app)
    print "Connected to DB."

