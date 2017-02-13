"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/bubble_match')
def index():
    """page to pick keywords of choice."""

    return render_template("bubble_match.html")








if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode
    connect_to_db(app)
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')


