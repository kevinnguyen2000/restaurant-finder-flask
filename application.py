from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import googlemaps

application = Flask(__name__)
application.secret_key = "top_secret_key"

API_KEY = "AIzaSyDuYX-inYNiuPI5UbgKbBBDu9vyAp3e5Ts"

map_client = googlemaps.Client(API_KEY)

home = "26 Augustine Terrace Glenroy, Victoria, Australia"
response = map_client.geocode(home)
print(response)

# route for home page
@application.route("/")
def home():
    return render_template("home.html")

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
