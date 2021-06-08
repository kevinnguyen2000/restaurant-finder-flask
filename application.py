from flask import Flask, render_template, request

application = Flask(__name__)
application.secret_key = "top_secret_key"

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
def map():
    return render_template("map.html")

if __name__ == "__main__":
    # application.run(debug=True)
    application.debug = True
    application.run()
