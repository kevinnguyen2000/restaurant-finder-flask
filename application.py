
from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
import logging
import googlemaps
import boto3
import json
from boto.s3.connection import S3Connection
import requests
from werkzeug.utils import secure_filename

application = Flask(__name__)
application.secret_key = "top_secret_key"
load_dotenv()
login_client_id = os.getenv('GOOGLE_CLIENT_ID')
login_secret = os.getenv('GOOGLE_CLIENT_SECRET')

# comment on live versions (not local)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id=login_client_id,
    client_secret=login_secret,
    reprompt_consent=True,
    scope=["profile","email"]
)

application.register_blueprint(blueprint, url_prefix="/login/")

API_KEY = os.getenv('GOOGLE_APIKEY')

map_client = googlemaps.Client(API_KEY)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')
table = dynamodb.Table('recommendations')

s3_client = boto3.client('s3')
bucket = "a3-review-images"

# route for home page
@application.route("/") 
def home():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()

        # assigning session to username
        session['username'] = google_data['name']

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

# route for map page
@application.route("/map/")
def mapview():

    # getting session username
    username = session['username']

    return render_template('map.html', username=username, API_KEY=API_KEY)

# route for map page
@application.route("/simpleMap/")
def simpleMapview():

    # getting session username
    username = session['username']

    return render_template('simpleMap.html', username=username, API_KEY=API_KEY)

# route for map page from reviews page
@application.route("/resMap/", methods=["POST", "GET"])
def resMapview():

    # getting session username
    username = session['username']

    if request.method == 'POST':
        resName = request.form['redirect']

        return render_template('resMap.html', username=username, resName=resName, API_KEY=API_KEY)

    else:
        return render_template('resMap.html', username=username, API_KEY=API_KEY)


# route for posts post
@application.route("/posts/")
def posts():

    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()

        # assigning session to username
        session['username'] = google_data['name']

    # getting session username
    username = session['username']

    # google id
    googleId = str(google_data['id'])

    # get all reviews from table
    reviews = table.scan()

    # get the number of reviews
    reviewNum = len(reviews['Items'])

    # get all images
    images = list()
    imgName = list()

    # getting artist name in format where we can call from s3
    for i in range(reviewNum):
        imgName = reviews["Items"][i]['imageName']
        images.append(imgName)

    return render_template('posts.html', username=username, google_data=google_data, reviewNum=reviewNum, reviews=reviews, images=images)

# route for writing a review
@application.route("/review/", methods=["POST", "GET"])
def review():

    if request.method == 'POST':
        user_info_endpoint = '/oauth2/v2/userinfo'
        if google.authorized:
            google_data = google.get(user_info_endpoint).json()

            # assigning session to username
            session['username'] = google_data['name']

        # getting session username
        username = session['username']

        # getting form inputs
        reviewTitle = request.form['reviewTitle']
        reviewRestaurant = request.form['reviewRestaurant']
        reviewText = request.form['reviewText']
        reviewImage = request.files['reviewImage']

        # google id
        googleId = str(google_data['id'])

        # image name
        imageName = googleId + "%25" + reviewRestaurant
        # format imageName for s3
        imageName = imageName.replace(" ","+")

        # put item in dynamodb
        table.put_item(
            Item={
                'reviewTitle': reviewTitle,
                'resName': reviewRestaurant,
                'reviewText': reviewText,
                'imageName': imageName
            }
        )

        # upload image

        filename = secure_filename(reviewImage.filename)
        reviewImage.save(filename)

        s3_client.upload_file(
            Bucket = bucket,
            Filename = filename,
            Key = str(googleId + "%" + reviewRestaurant)
            )

        # removes file
        os.remove(filename)

        # invoke api gateway
        url = "https://0qijwha2wc.execute-api.us-east-1.amazonaws.com/prod"

        headers = {"Content-Type": "application/json"}
        params = {"qs": "somevalue"}
        data_payload = {"payload": "payload"}

        r = requests.request("POST", url, params=params, data=data_payload)
        print(r.text)

        # get all reviews from table
        reviews = table.scan()

        # get the number of reviews
        reviewNum = len(reviews['Items'])

        # get all images
        images = list()
        
        # format imageName for s3
        imageName = imageName.replace(" ","+")

        # getting artist name in format where we can call from s3
        for i in range(reviewNum):
            imgName = reviews["Items"][i]['imageName']
            images.append(imgName)

        return render_template('posts.html', username=username, google_data=google_data, reviewNum=reviewNum, reviews=reviews, images=images)
    else:
        user_info_endpoint = '/oauth2/v2/userinfo'
        if google.authorized:
            google_data = google.get(user_info_endpoint).json()

            # assigning session to username
            session['username'] = google_data['name']

        # getting session username
        username = session['username']

        return render_template('review.html', username=username, google_data=google_data)

# function for handling lambda
def lamdba_handler(event, context, reviewTitle, reviewRestaurant, googleId, reviewText):
    bucket = 'a3-images'

    review = {}
    review['title'] = reviewTitle
    review['restaurant'] = reviewRestaurant
    review['text'] = reviewText
    review['user'] = googleId

    fileName = googleId + reviewRestaurant + '.json'
    uploadByteStream = bytes(json.dumps(review).encode('UTF-8'))

    s3.put_object(Bucket=bucket, Key=filename, Body=uploadByteStream)

if __name__ == "__main__":
    # application.run(debug=True)
    # application.debug = True
    application.run()
