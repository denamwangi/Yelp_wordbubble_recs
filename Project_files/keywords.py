"""THIS CODE IS FROM PYTEXTRANK CREATOR PACO's GITHUB. IT WAS ORIGINALLY SPLIT INTO
4 PARTS BUT COMBINING ALL 4 HERE AND ADAPTING FOR THIS PROJECT"""

#!/usr/bin/env python
# encoding: utf-8
import collections
import unicodedata
import sys
import math
import pytextrank           #Pulling in the pytext rank functions for each step.
from flask_sqlalchemy import SQLAlchemy
from json import dumps
from flask import Flask
from model import User, Business, Category, Location, BusinessCategoryLocation, Attribute, Review, Tip, Keyword, BusinessKeyword, BusinessSummary,  connect_to_db, db, app
DEBUG = False # True

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    connect_to_db(app)
    print "Connected to DB."



# Pull all the reviews from teh database for each restaurant and make that the relevant
# "corpus" or "document" that we will be analyzing for keywords.

# get all the businesses with a review
# Will do this for all cities but going to start with Toronto
businesses = (db.session.query(Review.business_id).
              join(BusinessCategoryLocation, Review.business_id == BusinessCategoryLocation.business_id).
              filter_by(city='Toronto', category='casual').
              group_by(Review.business_id).all())
print "HEEEEERE", businesses
i = 0
# BusinessKeyword.query.delete()
# BusinessSummary.query.delete()   
for business in businesses:
    if i<30:
        i += 1

        print "This is business", business.business_id
        reviews = db.session.query(Review.text).filter_by(business_id=business.business_id).all()
        reviews_list = []    #the list currently is of sql collection objects not strings. Need to unpack each
        reviews_json =collections.OrderedDict()     # textrank needs corpus in json form
        for review in reviews :
            reviews_list.append(review.text)
        reviews_corpus = ''.join(reviews_list)
        reviews_corpus.strip().replace('\n', '')
        reviews_corpus = unicodedata.normalize('NFD', reviews_corpus)
        reviews_corpus = reviews_corpus.encode('ascii', 'ignore')
        reviews_corpus = reviews_corpus.decode("utf-8")
        reviews_json['id'] = business.business_id
        reviews_json['text'] = reviews_corpus

        # print review_json
        test = dumps(reviews_json)
        # print type(test)
        sys.stdout=open('reviews.json',"w")
        print test
        sys.stdout.close()
        sys.stdout = sys.__stdout__

        print "START TEXT RANK"

    #ideally want to pass in reviews.json but have hardcoded to accomodate the QUEUE
        
        pytextrank_results = pytextrank.all_steps()     #This is a dictionary with 2 keys
        print "END TEXT RANK"


        pytextrank_keywords=pytextrank_results['keywords'].split(',') 
        for keyword in pytextrank_keywords:
            if '.' not in keyword:
                keyword = keyword.strip().lower()
                print keyword


        #Check if the keyword exists. 
                key_exist_check = Keyword.query.filter_by(keyword=keyword)

                
                if key_exist_check.first(): 
            # if exists, get the keyword id from the keyword table
                    
                    print "exists"
            # if doesnt exist. First add it to the keyword table
                else:

                    new_keyword = Keyword(keyword = keyword)
                    db.session.add(new_keyword)
                    # db.session.commit()
                    print "Doesnt exist so added: ",new_keyword


            #THEN- add the keyword to the BK table along with how many times? 
            # FIGURE OUT THE BEST WAY TO PULL THE COUNT

                keyword_id_obj = Keyword.query.filter_by(keyword=keyword).first()
                keyword_id = keyword_id_obj.keyword_id
                businesskeyword_entry = BusinessKeyword(business_id=business.business_id,
                                                        keyword_id= keyword_id,
                                                        keyword_count=20)
                
                
                                                
                db.session.add(businesskeyword_entry)
        summary_entry = BusinessSummary(business_id=business.business_id,
                                        summary = pytextrank_results['summary'])
        db.session.add(summary_entry)
        db.session.commit()

                # print keyword_id, keyword
                

    else:
        break
