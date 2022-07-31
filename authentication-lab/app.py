from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDjelXPa1M4Uib8qxuyyg5yYBG1l1wmIwM",
  "authDomain": "rephael-s-project.firebaseapp.com",
  "projectId": "rephael-s-project",
  "storageBucket": "rephael-s-project.appspot.com",
  "messagingSenderId": "526693248607",
  "appId": "1:526693248607:web:02fdd017f033f346db35ea",
  "measurementId": "G-7WRLLRF9ME",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		email = request.form["email"]
		password = request.form["password"]
	try:
		login_session['user'] = auth.sign_in_user_with_email_and_password(email, password)
		return redirect(url_for("add_tweet"))
	except:
		return render_template("signin.html")
    
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form["email"]
		password = request.form["password"]
	try:
		login_session['user'] = auth.create_user_with_email_and_password(email, password)
		return redirect(url_for("add_tweet"))
	except:
		return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
	login_session['user'] = None
	auth.current_user = None
	return redirect(url_for("signup"))



if __name__ == '__main__':
    app.run(debug=True)