
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

        return "<Business name=%s stars=%s >" % (self.business_id,
                                                 self.stars)


class Category(db.Model):
    """Categories- a business has multiple categories,
        multiple businesses in a category"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True)
    category = db.Column(db.String(120), primary_key=True, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category=%s >" % (self.category_id,
                                                           self.category)


class Location(db.Model):
    """Locations- multiple businesses in a location.
        seeding from the business json"""

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
    """Association table linking the business, category and location"""

    __tablename__ = "business_category_location"

    bcl_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String(120),
                            db.ForeignKey('businesses.business_id'),
                            nullable=False)
    category = db.Column(db.String(120),
                         db.ForeignKey('categories.category'),
                         nullable=False)
    city = db.Column(db.String(120),
                     db.ForeignKey('locations.city'),
                     nullable=False)
    state = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<BusinessCategoryLocation business_id=%s city=%s category=%s >" % (self.business_id,
                                                                                   self.state, self.category)


class Keyword(db.Model):
    """Keywords master table - each business can have multiple. These will be as
        a result of some NLP analysis"""

    __tablename__ = "keywords"

    keyword_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    keyword = db.Column(db.String(120), nullable=False)

    businesses = db.relationship('Business', secondary='businesses_keywords',
                                 backref='keywords')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Keyword keyword_id=%s keyword=%s >" % (self.keyword_id,
                                                        self.keyword)


class BusinessKeyword(db.Model):
    """Keywords and business Association Table  - each business can have multiple.
        These will be as a result of some NLP analysis with pytextrank"""

    __tablename__ = "businesses_keywords"

    buskey_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String(120), db.ForeignKey('businesses.business_id'), nullable=False)  # foreignkey
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.keyword_id'), nullable=False)
    keyword_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<BusinessKeyword business_id=%s keyword=%s >" % (self.business_id,
                                                                 self.keyword_count)


class BusinessSummary(db.Model):
    """Summary and business association table  - each business can have 1 summary.
        These will be as a result of some NLP analysis with pytextrank"""

    __tablename__ = "businesses_summaries"

    summ_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String(120), db.ForeignKey('businesses.business_id'), nullable=False)  # foreignkey
    summary = db.Column(db.String)
    
    businesses = db.relationship('Business', backref='summary')
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<BusinessSummary business_id=%s summ_id=%s >" % (self.business_id,
                                                                 self.summ_id)


class User(db.Model):
    """User data from the yelp data json."""

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
    """Reviews and Ratings of each establishment. Each business has at least one review"""

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


# def example_data():
#     """Example data to be used for testing"""
#     Business.query.delete()
#     BusinessCategoryLocation.query.delete()
#     Keyword.query.delete()
#     BusinessKeyword.query.delete()

#     business = Business(business_id="asdjhgsdfiu1234jfb",
#                         name="Dena's Deli",
#                         address="123 Main St.",
#                         latitude=37.7886679,
#                         longitude=-122.4114987,
#                         stars=5.0,
#                         review_count=12303,
#                         is_open=1)

#     kw = Keyword(keyword = "hipster")
#     kw2 = Keyword(keyword = "sunny")

#     bkw = BusinessKeyword(business_id="asdjhgsdfiu1234jfb",
#                             keyword_id=1,
#                             keyword_count=15)
#     bkw2 = BusinessKeyword(business_id="asdjhgsdfiu1234jfb",
#                             keyword_id=2,
#                             keyword_count=25)
#     loc = Location(city="San Francisco",
#                         state="CA",
#                         city_id=1)
#     category = Category(category="Dinner", category_id=1)

#     bcl = BusinessCategoryLocation(business_id="asdjhgsdfiu1234jfb",
#                                     city="San Francisco",
#                                     state="CA",
#                                     category="Dinner")

#     db.session.add(business) 
#     db.session.add(kw)
#     db.session.add(kw2)  
#     db.session.add(bkw)
#     db.session.add(bkw2) 
#     db.session.add(loc)
#     db.session.add(category, bcl)
#     # db.session.add(business)
#     db.session.commit()


##############################################################################
# Helper functions

def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///yelp'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
