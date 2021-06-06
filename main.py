from flask import Flask, render_template, request

app = Flask(__name__)

# route for home page
@app.route("/")
def home():
    return render_template("home.html")

# route for sign up page
@app.route("/signup/", methods=["POST", "GET"])
def signup():

    if request.method == 'POST':
        return render_template("signup.html")
    else:
        return render_template("signup.html")

# route for log in page
@app.route("/login/", methods=["POST", "GET"])
def login():
    
    if request.method == 'POST':
        return render_template("login.html")
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)