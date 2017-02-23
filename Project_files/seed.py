#This file will read in the various json files that are provided a part of the
#Yelp Data Challenge. It will create Classes for the data model used for the 
#project.

"""Utility file to seed ratings database from MovieLens data in seed_data/"""
from model import User, Business, Category, Location, BusinessCategoryLocation, BusinessPicture, Attribute, Review, Tip, Keyword, BusinessKeyword, connect_to_db, db, app
from datetime import datetime
import ast
import json
from pprint import pprint
import re
# # from server import app


def load_categories():
    """This parses a .txt file with all the possible categories pulled from yelp"""
    print "categories"
    with open('yelp_categories.txt', 'r') as cat_file:
      unique = {}
      i = 0
      for line in cat_file:
        cat_line=line.strip().split(' (')
        if cat_line[0] in unique:
          pass
        else:
          i += 1
          unique["%s" % cat_line[0]] = 1

          category = Category(category=cat_line[0].lower(), category_id = i)
          db.session.add(category)

      db.session.commit()


def iterate_json_file(stub_name, status_frequency= 500):
    i= 0
    with open('data/yelp_academic_dataset_%s.json' % stub_name, 'r') as f:
        for line in f:
            i += 1
            yield json.loads(line)               
            if i % status_frequency == 0:
                print("Status >>> : %d" % (i))

def load_pics():
  print "Pictures"
  c=0
  with open('data/yelp_academic_dataset_photo.json', 'r') as f:             # get a dictionary back
    #NEED SOME REGEX TO MAKE THIS WORK HERE. ITS ONE LONG STRING
    for line in f:
      new_line = re.sub("\[", '', line)
      new_line = re.sub('\]$', '', new_line)
    ##FIRST REPLACE THE BEGINING AND END [ ]

    ##THEN SPLIT IT UP INTO EACH SECTION STARTING WITH  { - COULDNT GET THIS RIGHT
    ##PATCHWORK HERE TO MAKE IT WORK
      split_string = re.split('{?},', new_line)
      # print "SPLIT MEEEEE ", split_string[2]
      #check on that last closing } that I couldnt figureout how to keep 
      for each_item in split_string:
        has_curly_brace = re.search('}$', each_item)
        # print has_curly_brace
        if has_curly_brace:
          fixed_string = re.sub("\[", "", each_item)
          fixed_string = "'"+fixed_string+"'"
        else:
          fixed_string = re.sub("\[", "", each_item)
          fixed_string = "'"+fixed_string+'}'+"'"

        # return fixed_string
        pdata = json.loads(fixed_string[1:-1])
        # import pdb; pdb.set_trace()
        # print pdata['photo_id']


        
        picture_exist = BusinessPicture.query.filter_by(business_id=pdata['business_id'])
        business_exist = Business.query.filter_by(business_id=pdata['business_id'])
        if business_exist.first():
          if picture_exist.first():
            print 'PICTURE EXISTS'

          elif c<300:
            print 'ADD NEW PICTURE'
            c += 1
            picture = BusinessPicture(picture=pdata['photo_id'],
                                      business_id=pdata['business_id'],
                                      caption=pdata['caption'],
                                      label=pdata['label'])
            db.session.add(picture)


            db.session.commit()
        else:
          print "BUSINESS DOES NOT EXIST ", pdata['business_id']



def load_businesses():
    print "Businesses"
    c=0
    unique={}
    i = 0

    #START ITERATING THROUGH EACH JSON
    for bdata in iterate_json_file('business'):             # get a dictionary back
        c += 1

    #START BUSINESS 
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
        db.session.add(business)
        db.session.commit()

  ## START LOCATIONS
        if bdata['city'] in unique:
          pass
        else:
          i+=1
          unique["%s" % bdata['city']] = 1

          location = Location(city=bdata['city'],
                              state = bdata['state'],
                              city_id= i)
          db.session.add(location)

          db.session.commit()
        # print "COMMIT LOCATION 128"


  #START ATTRIBUTE
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

                  # print "COMMIT ATTRIBUTE 157"

  #START CATEGORY-AUX
                  #Also want the option to play with having Attributes for ambiance 
                  #and goodformeal in the first category level search
                  if attribute_key in ['Ambience', 'GoodForMeal']:
    # First make sure its not in the master category table already
                    key_exist = Category.query.filter_by(category=subkeyval_pair[0].strip())
                    if key_exist.first():
                      pass
                    else:
            #If its not, add to category table with next number in sexuence
                      new_id = (Category.query.order_by('category_id desc').first().category_id) +1
                      category = Category(category=subkeyval_pair[0].strip(),
                                          category_id = new_id)
                      db.session.add(category)
                      db.session.commit()

                    businesscategorylocation = BusinessCategoryLocation(business_id=bdata['business_id'],
                                    city=bdata['city'],
                                    state=bdata['state'],
                                    category=subkeyval_pair[0].strip())
                    db.session.add(businesscategorylocation)


            #Case where it a key and value pair where the value is a single item
            elif attribute_value.strip()!= "False" and attribute_value.strip()!= "none" and attribute_key.strip()!="BusinessParking" and attribute_value.strip()!= "no":
              attribute = Attribute(business_id=bdata['business_id'],
                                  attribute_key=attribute_key.strip(),
                                  attribute_value=attribute_value.strip())
              db.session.add(attribute)

        if bdata['categories']:
          for each_item in bdata['categories']:
            each_item=each_item.lower()
#double check that the categories exist
            key_exist = Category.query.filter_by(category=each_item.lower())
            if key_exist.first(): 
              pass
            else:
                new_id = (Category.query.order_by('category_id desc').first().category_id) +1
                category = Category(category=each_item.lower(),
                                      category_id = new_id)
                db.session.add(category)
                db.session.commit()

                businesscategorylocation = BusinessCategoryLocation(business_id=bdata['business_id'],
                                  city=bdata['city'],
                                  state=bdata['state'],
                                  category=each_item.lower())
                db.session.add(businesscategorylocation)
        else:
          print "NO CATEGORY FOR THIS ONE: :<", bdata['name']    
          db.session.commit()


def load_users():
    print "Users"
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
        db.session.commit()

def load_tips():
  print "Tips"
  # Tip.query.delete()
  c=0
  for tdata in iterate_json_file('tip'):             # get a dictionary back
        
    business_key_exist = Business.query.filter_by(business_id=tdata['business_id'])
    if business_key_exist.first():
      c += 1
      tip = Tip(text=tdata['text'],
                  date=datetime_conversion(tdata['date']),
                  likes=tdata['likes'],
                  business_id=tdata['business_id'],
                  user_id=tdata['user_id'])
      db.session.add(tip)


      db.session.commit()

def load_reviews():

  """ADD EXTRA BIT WITH IF STAATEMENTS"""
  print "Reviews"
  c=0
  for rdata in iterate_json_file('review'):             # get a dictionary back
    
    review_exist = Review.query.filter_by(review_id=rdata['review_id'])
    if review_exist.first():
      pass
    else:    
      business_key_exist = Business.query.filter_by(business_id=rdata['business_id'])
      if business_key_exist.first():
                  # print "key exists already %s" % each_item
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
      else:
        pass
        
##############################################################################
# Helper functions

def datetime_conversion(datestring):
  """Converts our string dates to date time objects"""
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
    # print "LOAD CATEGORIES NOW"
    # load_categories()
    # print "DONE LOADING CATEGORIES"

    # print "LOAD BUSINESSES"
    # load_businesses()
    # print "DONE LOADING BUSINESSES"

    # print "LOAD USERS"
    # load_users()
    # print "LOAD USERS"

    # print "LOAD REVIEWS"
    # load_reviews()
    # print "LOAD REVIEWS"

    # print "LOAD TIPS"
    # load_tips()
    # print "LOAD TIPS"

    # print "LOAD PICS"
    # load_pics()
    # print "LOAD PICS"

    print "After loading EVERYTHING fingers crossed!!"
