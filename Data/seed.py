#This file will read in the various json files that are provided a part of the
#Yelp Data Challenge. It will create Classes for the data model used for the 
#project.

"""Utility file to seed ratings database from MovieLens data in seed_data/"""

# from sqlalchemy import func
# import model
from model import Review, User, Business, Tip, Category, Attribute, connect_to_db, db, app, BusinessCategoryLocation, Location

# # from server import app
from datetime import datetime
import ast




import json
from pprint import pprint
def load_categories():
    """This parses a .txt file with all the possible categories pulled from yelp"""
    print "categories"
    Category.query.delete()
    with open('yelp_categories.txt', 'r') as cat_file:
      unique={}
      i = 0
      for line in cat_file:
        cat_line=line.strip().split(' (')
        # print cat_line[0]
        
        if cat_line[0] in unique:
          pass
        else:
          i+=1
          unique["%s" % cat_line[0]] = 1

          category = Category(category=cat_line[0].lower(), category_id = i)
          db.session.add(category)

      db.session.commit()

def load_locations():
    """This parses a .txt file with all the cities from teh datachelenge and codes I added"""
    print "locations"
    Location.query.delete()
    with open('yelp_locations.txt', 'r') as cat_file:
      unique={}
      i = 0
      for line in cat_file:
        city_line=line.strip().split(',')
        
        if city_line[3] in unique:
          pass
        else:
          i+=1
          unique["%s" % city_line[3]] = 1

          location = Location(city=city_line[0].lower(),
                              state = city_line[1].lower(),
                              country = city_line[2].lower(),
                              city_id= city_line[3].lower())
          db.session.add(location)

      db.session.commit()


def iterate_json_file(stub_name, status_frequency= 500):
    i= 0
    with open('yelp_academic_dataset_%s.json' % stub_name, 'r') as f:
        for line in f:
            i += 1
            # print line
            # data= json.loads(line)
            yield json.loads(line)                  
            if i % status_frequency == 0:
                print("Status >>> : %d" % (i))
                # if i == 300:
                #     raise StopIteration()


def load_businesses():
    print "Businesses"
    Attribute.query.delete()
    BusinessCategoryLocation.query.delete()
    Business.query.delete()

    c=0
    for bdata in iterate_json_file('business'):             # get a dictionary back
        c += 1
        business = Business(business_id=bdata['business_id'],
                           name=bdata['name'],
                           neighborhood=bdata['neighborhood'],
                           address=bdata['address'],
                           postal_code=bdata['postal_code'],
                           latitude=bdata['latitude'],
                           longitude=bdata['longitude'],
                           stars=bdata['stars'],
                           review_count=bdata['review_count'],
                            is_open=True if bdata['is_open'] == 1 else False)
        # print "ATTRIBUTES:", bdata['attributes']

        #Pull out categories here and add create an instance of the Category class
        if bdata['categories']:
          for each_item in bdata['categories']:
              # print bdata['categories']
              businesscategorylocation = BusinessCategoryLocation(business_id=bdata['business_id'],
                                  city=bdata['city'],
                                  state=bdata['state'],
                                  category=each_item.lower())
        else:
            businesscategorylocation = BusinessCategoryLocation(business_id=bdata['business_id'],
                                city=bdata['city'],
                                state=bdata['state'],
                                )
            # db.session.add(businesscategorylocation)

        #Pull out attributes here and add create an instance of the Category class
        if bdata['attributes']:
          for each_item in bdata['attributes']:
            attribute_key=each_item.split(':',1)[0]
            attribute_value=each_item.split(':', 1)[1]

            #case where the value is a string in the form of a dictionary
            # Good for meal, ambiance, HairSpecializesIn

            if attribute_key in ['HairSpecializesIn', 'Ambience', 'GoodForMeal']:
              attribute_value = attribute_value.replace('{', '').replace('}', '').replace("'", '')
              parsed_value = attribute_value.split(',')

              #Now each item in the list is a string key: val pair. Will need to split again
              # then the first index contains the key and second index contains the value
              for subkeyval_pair in parsed_value:
                subkeyval_pair = subkeyval_pair.strip().split(':')
                # print subkeyval_pair[0], subkeyval_pair[1]
                if subkeyval_pair[1].strip() != "False" and subkeyval_pair[1].strip() != "none" and subkeyval_pair[1].strip() != "no":
                  # print subkeyval_pair[1], type(subkeyval_pair[1])
                  attribute = Attribute(business_id=bdata['business_id'],
                                      attribute_key=subkeyval_pair[0].strip(),
                                      attribute_value=subkeyval_pair[1].strip())
                  db.session.add(attribute)

            #Case where it a key and value pair where the value is a single item
            elif attribute_value.strip()!= "False" and attribute_value.strip()!= "none" and attribute_key.strip()!="BusinessParking" and attribute_value.strip()!= "no":
              attribute = Attribute(business_id=bdata['business_id'],
                                  attribute_key=attribute_key.strip(),
                                  attribute_value=attribute_value.strip())
              db.session.add(attribute)

        db.session.add(business)
        db.session.commit()


def load_users():
    print "Users"
    User.query.delete()
    c= 0
    for udata in iterate_json_file('user'):             # get a dictionary back
        c += 1
        user= User(user_id=udata['user_id'], 
                   name=udata['name'],
                   review_count=udata['review_count'],
                   yelping_since=udata['yelping_since'],
                   friends=udata['friends'],
                   useful=udata['useful'],
                   funny=udata['funny'],
                   cool=udata['cool'],
                   fans=udata['fans'],
                   elite=udata['elite'],
                   average_stars=udata['average_stars'],
                   compliment_hot=udata['compliment_hot'],
                   compliment_more=udata['compliment_more'],
                   compliment_profile=udata['compliment_profile'],
                   compliment_cute=udata['compliment_cute'],
                   compliment_list=udata['compliment_list'],
                   compliment_note=udata['compliment_note'],
                   compliment_plain=udata['compliment_plain'],
                   compliment_cool=udata['compliment_cool'],
                   compliment_funny=udata['compliment_funny'],
                   compliment_writer=udata['compliment_writer'],
                   compliment_photos=udata['compliment_photos'])
        db.session.add(user)
        # print "Success", udata['user_id']
    db.session.commit()

def load_tips():
    print "Tips"
    Tip.query.delete()
    c=0
    for tdata in iterate_json_file('tip'):             # get a dictionary back
        c += 1
        tip=Tip(text=tdata['text'],
                date=datetime_conversion(tdata['date']),
                likes=tdata['likes'],
                business_id=tdata['business_id'],
                user_id=tdata['user_id'])
        db.session.add(tip)


    db.session.commit()

def load_reviews():
    print "Reviews"
    Review.query.delete()
    c=0
    for rdata in iterate_json_file('review'):             # get a dictionary back
        c += 1
        review = Review(review_id=rdata['review_id'],
                        user_id=rdata['user_id'], 
                        business_id=rdata['business_id'],
                        stars=rdata['stars'],
                        date=datetime_conversion(rdata['date']),
                        text=rdata['text'],
                        useful=rdata['useful'],
                        funny=rdata['funny'],
                        cool=rdata['cool'], )
        db.session.add(review)

    db.session.commit()
##############################################################################
# Helper functions
# def init_app():
#     # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
#     from flask import Flask
#     app= Flask(__name__)

#     connect_to_db(app)
#     print "Connected to DB."
def datetime_conversion(datestring):
    try: 
        date_object = datetime.strptime(datestring, '%Y-%b-%d').date()
        return date_object
    except ValueError:
        return

if __name__ == "__main__":
    # db.app=app
    # db.init_app(app)
    connect_to_db(app)
    db.create_all()
    load_categories()
    load_locations()
    # load_businesses()
    # load_users()
    # load_reviews()
    # load_tips()
    print "After loading businesses fingers crossed!"
#     # As a convenience, if we run this module interactively, it will leave
#     # you in a state of being able to work with the database directly.

#     # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
#     from flask import Flask

#     app= Flask(__name__)

#     connect_to_db(app)
#     print "Connected to DB."



# ********************************************************************************
# def load_users():
#     """Load users from u.user into database."""

#     print "Users"

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     User.query.delete()

#     # Read u.user file and insert data
#     for row in open("seed_data/u.user"):
#         row= row.rstrip()
#         user_id, age, gender, occupation, zipcode= row.split("|")

#         user= User(user_id=user_id,
#                     age=age,
#                     zipcode=zipcode)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(user)

#     # Once we're done, we should commit our work
#     db.session.commit()


# def load_movies():
#     """Load movies from u.item into database."""
#     def datetime_conversion(datestring):
#         try: 
#             date_object= datetime.strptime(datestring, '%d-%b-%Y').date()
#             return date_object
#         except ValueError:
#             return
  
#     def delete_title_year(movie_title):
#         if len(movie_title) > 1:
#             return "".join(movie_title[:-1])
#         else:
#             return movie_title[0]

#     print "Movies"

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Movie.query.delete()

#     # Read u.user file and insert data
#     for row in open("seed_data/u.item"):
#         row= row.rstrip()
#         movie_list= row.split("|")

#         movie= Movie(movie_id=movie_list[0],
#                     title=delete_title_year(movie_list[1].split('(')),
#                     released_at=datetime_conversion(movie_list[2]),
#                     imdb_url=movie_list[4])

#         # We need to add to the session or it won't ever be stored
#         db.session.add(movie)

#     # Once we're done, we should commit our work
#     db.session.commit()

# def load_ratings():
#     """Load ratings from u.data into database."""

#     print "Ratings"

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Rating.query.delete()

#     # Read u.user file and insert data
#     for row in open("seed_data/u.data"):
#         row= row.rstrip()
#         user_id, movie_id, score, timestamp= row.split("\t")

#         rating= Rating(movie_id=movie_id,
#             user_id=user_id,
#             score=score)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(rating)

#     # Once we're done, we should commit our work
#     db.session.commit()


# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result= db.session.query(func.max(User.user_id)).one()
#     max_id= int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query= "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()



#     # In case tables haven't been created, create them
#     db.create_all()

#     # Import different types of data
#     load_users()
#     load_movies()
#     load_ratings()
