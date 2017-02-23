
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension

from flask.ext.triangle import Triangle
from model import User, Business, Category, Location,  Attribute, Review, Tip, Keyword, BusinessKeyword, connect_to_db, db
from model import BusinessCategoryLocation as BCL 
from random import choice, sample
app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined
Triangle(app)

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
                                  filter_by(city='Toronto', category='dinner').\
                                  group_by(Business.business_id).limit(20).all()

    businesses = sample(businesses, 5)
    results={}
    i=0
    for business in businesses:
        # print "Business keywords: ", business.keywords
        nlp_keywords =[]
        for keyword_object in business.keywords:
            nlp_keywords.append(keyword_object.keyword)
        nlp_summary = business.summary[0].summary
        # print "HEEEERE",
        i+=1
        results['option%s' % i] = {"name" : business.name.lower(),
                                    "business_id" : business.business_id,
                                    "latitude" : business.latitude,
                                    "longitude" : business.longitude,
                                    "stars" : business.stars,
                                    "nlp_keywords" : nlp_keywords,
                                    "nlp_summary" : nlp_summary} 
    # print "READ MEEEE", results
    return jsonify(results)

### ROUTE THAT DISPLAYS THE HTML FOR THE RESULTS PAGE. FOR NOW ITS
### JUST THE JSON IN THE DIVS. WILL BE D3. ALSO HAS MAP OF RESULTS
### NEED TO FIGURE OUT PAGINATION HERE(PHASE 2)
###             FEATURES: D3 IMAGE OF RESULTS; MAP WITH GEOLOCATION

@app.route('/results', methods=['GET'] )
def keyword_choice():
    """Displays search results of restaurant search."""


    return render_template("results.html")

@app.route('/selected')
def results():
    """Selected restaurant."""

    form_results=request.args.get.im_self

    for each_chosen in form_results.keys():
        print 'yay', dir(form_results[each_chosen])
        final_pick=form_results[each_chosen]
        print 'yay you picked', final_pick


    return render_template("selected.html", final_pick = final_pick)

@app.route('/map_play')
def map_play():
    """Displays search results of restaurant search."""


    return render_template("test_googlemaps.html")

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
