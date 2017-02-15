"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Business, Category, Location,  Attribute, Review, Tip, Keyword, BusinessKeyword, connect_to_db, db
from model import BusinessCategoryLocation as BCL 

app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def index():
    """Homepage."""
    states = db.session.query(BCL.state).group_by(BCL.state).all()
    print "THIS IS THE OUTPUT FOR states: "
    print states

    return render_template("homepage.html", states=states)


@app.route('/bubble_match', methods=['GET'] )
def keyword_choice():
    """page to pick keywords of choice."""
    state = request.args.get("state")
    category = request.args.get("category")
    print state

    return render_template("bubble_match.html", 
                            state=state, 
                            category=category)


@app.route('/results')
def results():
    """results with personalized recommendations."""

    return render_template("results.html")



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode
    connect_to_db(app)
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')


