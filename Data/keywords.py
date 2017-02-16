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
from model import User, Business, Category, Location, BusinessCategoryLocation, Attribute, Review, Tip, Keyword, BusinessKeyword, connect_to_db, db, app
DEBUG = False # True

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    connect_to_db(app)
    print "Connected to DB."



#Pull all the reviews from teh database for each restaurant and make that the relevant
# "corpus" or "document" that we will be analyzing for keywords.

#get all the businesses with a review
businesses = db.session.query(Review.business_id).group_by(Review.business_id).all()
i=0

    
for business in businesses:
    while i<1:
        i += 1

        print business.business_id
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

        # print "START STEP 1"
    pytextrank.step_1('reviews.json')
        # print "START STEP 2"
    pytextrank.step_2('output1.json', 'output2.json')



# testcase = db.session.query(Review).first()
# print testcase.business_id
# reviews = db.session.query(Review.text).filter_by(business_id=testcase.business_id).all()
# print reviews

# review_list = []
# for review in reviews :

#     review_list.append(review.text)
# print review_list
# review_corpus = ''.join(review_list)
# print review_corpus
#In json form pass that through to step1 of the pytextrank functions and have that run


#This will need to be a loop for each business (category??)


#Example with sample json here
# step_1('dat/mih.json', 'out1.json')
# step_2('out1.json', 'out2.json')
# step_3('out1.json', 'out2.json', 'out3.json')
# step_4('out2.json', 'out3.json', 'out4.json')





##############################################################################
# Helper functions





