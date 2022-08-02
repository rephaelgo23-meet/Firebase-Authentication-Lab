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
  "databaseURL": "https://rephael-s-project-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

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
		full_name = request.form["full_name"]
		username = request.form["username"]
		bio = request.form["bio"]
		user = {
			"full_name": full_name,
			"user": username,
			"bio": bio
		}
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			db.child("users").child(login_session['user']['localId']).set(user)
			return redirect(url_for("add_tweet"))
		except:
			print("im getting an error")
			return render_template("signup.html")
	else:
		return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		title = request.form["title"]
		text = request.form["text"]
		tweet = {"title": title, "text": text}
		db.child("tweets").push(tweet)
	return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
	tweets = db.child("tweets").get().val()
	return render_template("tweets.html", tweets=tweets)

@app.route('/signout', methods=['GET', 'POST'])
def signout():
	login_session['user'] = None
	auth.current_user = None
	return redirect(url_for("signup"))



if __name__ == '__main__':
    app.run(debug=True)