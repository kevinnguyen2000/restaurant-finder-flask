
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
import logging
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import googlemaps


application = Flask(__name__)
application.secret_key = "top_secret_key"
load_dotenv()
login_client_id = os.getenv('GOOGLE_CLIENT_ID')
login_secret = os.getenv('GOOGLE_CLIENT_SECRET')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id=login_client_id,
    client_secret=login_secret,
    reprompt_consent=True,
    scope=["profile","email"]
)

application.register_blueprint(blueprint, url_prefix="/login/")

API_KEY = "AIzaSyDuYX-inYNiuPI5UbgKbBBDu9vyAp3e5Ts"

map_client = googlemaps.Client(API_KEY)

home = "26 Augustine Terrace Glenroy, Victoria, Australia"
response = map_client.geocode(home)
print(response)

# route for home page
@application.route("/") 
def home():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()

    return render_template("home.html", google_data=google_data,fetch_url=google.base_url + user_info_endpoint)



# route for sign up page
@application.route("/signup/", methods=["POST", "GET"])
def signup():

    if request.method == 'POST':
        return render_template("signup.html")
    else:
        return render_template("signup.html")

# route for log in page
@application.route("/login/", methods=["POST", "GET"])
def login():
    
    if request.method == 'POST':
        return render_template("login.html")
    else:
        return render_template("login.html")

# route for google log in 
@application.route("/googlelogin/", methods=["POST", "GET"])
def googleLogin():
    
    if request.method == 'POST':
        return redirect(url_for('google.login'))
    else:
        return redirect(url_for('google.login'))

# route for logging out of google account
@application.route("/googlelogout/", methods=["POST", "GET"])
def googleLogout():

    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'

    return render_template("home.html", google_data=google_data,fetch_url=google.base_url + user_info_endpoint)

# route for account page
@application.route("/account/", methods=["POST", "GET"])
def account():
    
    if request.method == 'POST':
        return render_template("account.html")
    else:
        return render_template("account.html")

# route for account page
@application.route("/map/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    
    return render_template('map.html', mymap=mymap)

if __name__ == "__main__":
    # application.run(debug=True)
    application.debug = True
    application.run()
