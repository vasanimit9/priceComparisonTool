from flask import render_template, request, redirect, session, escape
from app import app
from tinydb import TinyDB, where
from scrapers import scraper
import random
from mailer import Mailer
from credentials import login_, password_
import time
from category import categories as cats
import hashlib

db = TinyDB('database.json')
initial_time = db.search(where('initial_time'))[0]['initial_time']
mailer1 = Mailer(login_, password_)
def secure_hash(string):
	return hashlib.sha512(string.encode()).hexdigest()

@app.route('/')
@app.route('/index')
def index():
	if 'email' in session:
		print("Current user:", session['email'])
		return render_template('index.html', title='Home', msgs=request.args.get('msgs'),
		 categories = cats, user = session['email'])
	return render_template('index.html', title='Home', categories = cats,
	 msgs=request.args.get('msgs'))

@app.route('/search', methods = ['get', 'post'])
def search():
	s = request.args.get('s')
	if s!=None:
		s = " ".join(s.split("%20"))
		scrap = scraper(s)
		if 'email' in session:
			return render_template('search.html', title = s, output=scrap.products, 
				sstring = s, msgs = request.args.get('msgs'), categories = cats,
				 user = session['email'])
		else:
			return render_template('search.html', title = s, output=scrap.products, 
				sstring = s, msgs = request.args.get('msgs'), categories = cats)
	else:
		return redirect('/index')

@app.route('/sign_up', methods = ['get', 'post'])
def sign_up():
	if not 'email' in session:
		return render_template("sign_up.html", title="Sign Up",
		 msgs = request.args.get('msgs'))
	else:
		return redirect('/index')

@app.route('/register', methods = ['get', 'post'])
def register():
	# username = request.form.get('username')
	email = request.form.get('email')
	if email != None and not db.contains(where('email')==email):
		temp_password = str(random.random()*1000000)
		db.insert({"type": "user", "email": email,
		 "password_hash": secure_hash(temp_password)})
		mailer1.sendRegistrationMail(email, temp_password)
		return redirect('/sign_up?msgs=Check email for password')
	else:
		return redirect('/sign_up?msgs=Email already taken')
	return redirect('/index')


@app.route('/login', methods = ['get', 'post'])
def login():
	if 'email' not in session:
		msgs = request.args.get('msgs')
		if msgs:
			return render_template('login.html', title='Log in', msgs = msgs)
		else:
			return render_template('login.html', title='Log in')
	else:
		return redirect('/index')

@app.route('/validate_login', methods = ['get', 'post'])
def validate_login():
	email = request.form.get('email')
	password_hash = secure_hash(request.form.get('password'))
	if db.contains(where('email') == email):
		records = db.search(where('email') == email)
		print(records[0]['password_hash'])
		print(password_hash)
		if records[0]['password_hash'] == password_hash:
			session["email"] = email
			session["password_hash"] = password_hash
			print('%s logged in'%email)
			return redirect('index')
		else:
			return redirect('login?msgs=Invalid password')
	else:
		return redirect('login?msgs=Invalid email')

@app.route('/logout')
def logout():
	if 'email' in session:
		print('%s logged out'%session['email'])
		session.pop('email')
	return redirect('/index')

@app.route('/change_password', methods = ['get', 'post'])
def change_password():
	email = request.args.get('email')
	email = "@".join(email.split("%40"))
	password_hash = request.args.get('h')
	if db.contains((where('email') == email) & (where('password_hash') == password_hash)):
		if 'email' in session:
			return render_template('change_password.html', title='Change Password',
		 email = email, h = password_hash, user = session['email'])
		else:
			return render_template('change_password.html', title='Change Password',
		 email = email, h = password_hash)
	else:
		return redirect('login?msgs=Link expired')

@app.route('/change', methods = ['post', 'get'])
def change():
	email = request.args.get('email')
	email = "@".join(email.split("%40"))
	password_hash = request.args.get('h')
	new_password_hash = secure_hash(request.form.get('password'))
	db.update({"password_hash": new_password_hash}, 
		(where('email') == email) & (where('password_hash') == password_hash))
	return redirect('/logout')

@app.route('/forgot_password', methods = ['post', 'get'])
def forgot_password():
	try:
		email = session['email']
	except:
		email = request.args.get('email')
		email = "@".join(email.split("%40"))
	print(email)
	if db.contains(where('email') == email):
		password_hash = db.search(where('email') == email)[0]['password_hash']
		print('password_hash')
		mailer1.sendMail(to = email, subject = "Password reset link", body = '''
			<a href='%s/change_password?email=%s&h=%s'>Reset Password</a>
			'''%('/'.join(request.base_url.split("/")[:-1]), email, password_hash))
		return redirect('/index?msgs=Check mail for Password Reset Link')
	else:
		return redirect('/login?msgs=Invalid email')

@app.route('/subscribe', methods = ['post', 'get'])
def subscribe():
	try:
		if 'email' in session:
			link = request.form.get('link')
			source = request.form.get('source')
			t = int(request.form.get('time'))
			name = request.form.get('name')
			if db.contains((where('name') == name) & (where('email') == session['email'])
			 & (where('link') == link) & (where('time') == t)):
				return 'Notification already set before'
			if db.insert({"type":"notification", "name": name ,"email": session['email'],
			 "link": link, "source": source, "time": t}):
				return 'Notification set'
			else:
				return 'Some error occurred'
		else:
			return 'You must login to subscribe to notifications'
	except:
		return 'Some error occurred'

@app.route('/profile')
def profile():
	if 'email' in session:
		output = db.search((where('type') == 'notification') & 
			(where('email') == session['email']))
		return render_template('profile.html', title = 'Profile', output = output,
		 user = session['email'], msgs = request.args.get('msgs'))
	else:
		return redirect('/index');

@app.route('/unsubscribe', methods = ['post', 'get'])
def unsubscribe():
	if 'email' in session:
		link = request.form.get('link')
		t = int(request.form.get('time'))
		email = session['email']
		if db.remove((where('email') == email) & (where('link') == link) & (where('time')==t)):
			return './profile?msgs=Unsubscribed successfully'
		else:
			return './profile?msgs=Some error occurred'
	else:
		return './index?msgs=Some error occurred'

@app.route('/categories', methods = ['get'])
def categories():
	if 'email' in session:
		return render_template('categories.html', title = "categories", categories = cats,
		 msgs = request.args.get('msgs'), user = session['email'])
	else:
		return render_template('categories.html', title = "categories", categories = cats,
		 msgs = request.args.get('msgs'))

@app.route('/start_recording', methods = ['get', 'post'])
def start_recording():
	product_name = request.form.get('name')
	product_link = request.form.get('link')

