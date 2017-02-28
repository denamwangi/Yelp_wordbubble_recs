
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension

from flask.ext.triangle import Triangle
from model import User, Business, Category, Location,  Attribute, Review, Tip, Keyword, BusinessKeyword, connect_to_db, db
from model import BusinessCategoryLocation as BCL 
from random import choice, sample
import sys
import os
app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined
Triangle(app)


google_api_key= os.environ['GOOGLE_MAPS_API_KEY']
print "GOOGLE KEY", google_api_key

### ROUTE FOR HOME PAGE. 
###             FEATURE: SEARCH BAR - CATEGORY AND LOCATION
@app.route('/')
def index():
    """Homepage."""

    states = db.session.query(BCL.state).group_by(BCL.state).all()
    print "THIS IS THE OUTPUT FOR states: "
    print states

    return render_template("homepage.html", states=states)

### ROUTE THAT SEARCHES DATABASE ADN RETURNS JSON OF POTENTIAL RESTAURANTS

@app.route('/restaurants_search.json', methods=['GET'] )
def restaurant_pics():
    """search database and return search results in json"""

    state = request.args.get("state")
    category = request.args.get("category")

    businesses = db.session.query(Business).\
                                  join(BusinessKeyword, BCL).\
                                  filter_by(city='Las Vegas').\
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
        # print "HEEEERE",
        all_lats.append(business.latitude)
        all_lngs.append(business.longitude)
        
 
        results['option%s' % i] = {"name" : business.name.lower(),
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

# @app.route('/selected.json')
# def selected_json():
#     """Selected restaurant json with helpful information """
#     final_pick={}
#     form_results=request.args.get.im_self
#     for each_chosen in form_results.keys():
#         business_id=form_results[each_chosen]
#     business = db.session.query(Business).\
#                                   join(BCL).\
#                                   filter_by(business_id=business_id).\
#                                   group_by(Business.business_id).first()
    
#     final_pick['business_id']=business_id
#     final_pick['name']=business.name
#     final_pick['latitude']=business.latitude
#     final_pick['longitude']=business.longitude
#     final_pick['stars']=business.stars
#     redirect('/selected')
#     return jsonify(final_pick)

    # return render_template("selected.html", final_pick = final_pick)

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
    
    final_pick['business_id']=business_id
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


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode
    connect_to_db(app)
    DebugToolbarExtension(app)
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
