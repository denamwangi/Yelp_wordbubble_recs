
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension

from flask.ext.triangle import Triangle
from model import User, Business, Category, Location,  Attribute, Review, Tip, Keyword, BusinessKeyword, connect_to_db, db
from model import BusinessCategoryLocation as BCL 
from random import choice, sample
import sys
import os
from sqlalchemy import func
from sqlalchemy.sql import label
from twilio.rest import TwilioRestClient


app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined
Triangle(app)


google_api_key= os.environ['GOOGLE_MAPS_API_KEY']
twilio_api_key= os.environ['TWILIO_API_KEY']
twilio_acct_sid= os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token= os.environ['TWILIO_AUTH_TOKEN']
twilio_my_phone= os.environ['TWILIO_MY_PHONE']


### ROUTE FOR HOME PAGE. 
###             FEATURE: SEARCH BAR - CATEGORY AND LOCATION
@app.route('/')
def index():
    """Homepage."""

    states = (db.session.query(BCL.city, BCL.category, 
        label('cat_count', func.count(BCL.category))).
        group_by(BCL.city, BCL.category).all())    

    cities = ["Charlotte", "Las Vegas", "Montreal", "Pittsburgh", "Phoenix",  "Toronto"]

    return render_template("homepage.html", cities=cities)

@app.route('/category_count.json')
def category_count():
    """Returns a list of tuples with category counts."""

    # category_weighted = db.session.execute('SELECT * FROM category_counts_by_city WHERE count>1').fetchall()
    # print category_weighted
    category_weighted  = (db.session.query(BCL.city, BCL.category, 
        label('cat_count', func.count(BCL.category))).
        group_by(BCL.city, BCL.category).all())   
    city = request.args.get("search_city")
    # city = 'Toronto'
    print "CITY IS" ,city
    category_count_list=[]
    i=0
    for each_item in category_weighted :
        city_server = each_item[0]
        category_name = each_item[1]
        category_count = each_item[2]
        if city_server==city and category_count>1:
            i+=1

            cat_obj= {"text": category_name,
                        "size" : category_count,
                        "group": "2"}
            category_count_list.append(cat_obj)

    # import pdb; pdb.set_trace()
    print "CATEGORY IS", type(category_count_list)   
    return jsonify(category_count_list)

### ROUTE THAT SEARCHES DATABASE AND RETURNS JSON OF POTENTIAL RESTAURANTS

@app.route('/restaurants_search.json', methods=['GET'] )
def restaurant_pics():
    """search database and return search results in json"""

    city = request.args.get("city")
    category = request.args.get("category")

    businesses = db.session.query(Business).\
                                  join(BusinessKeyword, BCL).\
                                  filter_by(city='Toronto').\
                                  group_by(Business.business_id).limit(20).all()

    businesses = sample(businesses, 10)
    results={}
    i=0
    all_lats = []
    all_lngs = []
    for business in businesses:
        # print "Business keywords: ", business.keywords
        nlp_keywords =[]
        for keyword_object in business.keywords:
            #need each of these to be an object here to go through
            # D3 using template. Leaving room for including a size
            # factor from the NLP analysis
            kw_obj = {"text": keyword_object.keyword,
                        "size" : "20",
                        "group": "1"}

            nlp_keywords.append(kw_obj)
        nlp_summary = business.summary[0].summary
        nlp_summary=nlp_summary.split('.')
        nlp_summary='. '.join(nlp_summary)
        print "HEEEERE", nlp_summary
        all_lats.append(business.latitude)
        all_lngs.append(business.longitude)
        
 
        results['option%s' % i] = {"name" : business.name,
                                    "business_id" : business.business_id,
                                    "latitude" : business.latitude,
                                    "longitude" : business.longitude,
                                    "stars" : business.stars,
                                    "nlp_keywords" : nlp_keywords,
                                    "nlp_summary" : nlp_summary} 
        i+=1

        #calculate the center of the map here

    center_lat = sum(all_lats)/len(all_lats)
    center_lng = sum(all_lngs)/len(all_lngs)
    print "HEEERE", center_lat, center_lng
    return jsonify(results)

### ROUTE THAT DISPLAYS THE HTML FOR THE RESULTS PAGE. FOR NOW ITS
### JUST THE JSON IN THE DIVS. WILL BE D3. ALSO HAS MAP OF RESULTS
### NEED TO FIGURE OUT PAGINATION HERE(PHASE 2)
###             FEATURES: D3 IMAGE OF RESULTS; MAP WITH GEOLOCATION

@app.route('/results', methods=['GET'] )
def keyword_choice():
    """Displays search results of restaurant search."""


    return render_template("results.html", google_api_key = google_api_key)


@app.route('/selected')
def results():
    """Selected restaurant."""
    final_pick={}
    form_results=request.args.get.im_self
    # print form_results
    for each_chosen in form_results.keys():
        business_id=form_results[each_chosen]
    business = db.session.query(Business).\
                                  join(BCL).\
                                  filter_by(business_id=business_id).\
                                  group_by(Business.business_id).first()
    
    final_pick['business_id']=business.business_id
    final_pick['name']=business.name
    final_pick['latitude']=business.latitude
    final_pick['longitude']=business.longitude
    final_pick['stars']=business.stars
    # redirect('/selected')
    print google_api_key
    print final_pick
    return render_template("selected.html", 
                            final_pick=final_pick, 
                            google_api_key = google_api_key)

@app.route('/twilio.json')
def twilio_request():
    """Texts users the results."""
    twilio_client = TwilioRestClient(twilio_acct_sid, twilio_auth_token)
    user_phone = request.args.get("user_phone")
    business_name= request.args.get("business_name")
    print type(user_phone), user_phone, twilio_my_phone

    twilio_client.messages.create(
        to="+1%s" % user_phone,
        from_= twilio_my_phone,
        body = "You're all set for %s" % business_name,
        )
    message = ["All good"]
    return jsonify(message)







if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode
    connect_to_db(app)
    db.create_all(app=app)
    # DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')


            #### PHASE 2 OF PROJECT AFTER MVP

### ROUTE THAT DOES THINGS WITH THE FINAL RESTAURANT YOU CHOSE
###     FEATURES: TEXTS YOU THE NAME AND ADDRESS? CALLS A LYFT?


### ROUTE THAT RETURNS MORE INFO ON THE RESTAURANT. PHASE 2- MENU? IS THERE AN API?
###             FEATURES: MENU FROM API?
# @app.route('/results/<restaurant_name>', methods=['GET'] )
# def keyword_choice():
#     """Displays more info on the restaurant."""



#     return render_template("results_detail.html")
