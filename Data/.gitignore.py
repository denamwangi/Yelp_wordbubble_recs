#This file will read in the various json files that are provided a part of the
#Yelp Data Challenge. It will create Classes for the data model used for the 
#project.

"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
import model
# from model import Review, User, Business, Tip, Category, Attribute
# from model import connect_to_db, db
# from server import app
from datetime import datetime



"""
TO DO LIST:
- SET UP SEEDING IN FUNCTIONS
-INCLUDE THE COUNTERS
"""
import json
from pprint import pprint

with open('yelp_academic_dataset_business.json', 'r') as f:
    for line in f:
        print line
        data = json.loads(line)


********************************************************************************
def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    def datetime_conversion(datestring):
        try: 
            date_object = datetime.strptime(datestring, '%d-%b-%Y').date()
            return date_object
        except ValueError:
            return
  
    def delete_title_year(movie_title):
        if len(movie_title) > 1:
            return "".join(movie_title[:-1])
        else:
            return movie_title[0]

    print "Movies"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Movie.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        movie_list = row.split("|")

        movie = Movie(movie_id=movie_list[0],
                    title=delete_title_year(movie_list[1].split('(')),
                    released_at=datetime_conversion(movie_list[2]),
                    imdb_url=movie_list[4])

        # We need to add to the session or it won't ever be stored
        db.session.add(movie)

    # Once we're done, we should commit our work
    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Rating.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, movie_id, score, timestamp = row.split("\t")

        rating = Rating(movie_id=movie_id,
            user_id=user_id,
            score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
