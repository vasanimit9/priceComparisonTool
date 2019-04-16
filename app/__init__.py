from flask import Flask
import time
from datetime import datetime, timezone
import pytz
from tinydb import TinyDB, where
from scrapers import extractPrice
from mailer import Mailer
from credentials import login_, password_, secret_key
import threading

db = TinyDB('database.json')

app = Flask(__name__)
app.secret_key = secret_key

def background_jobs():
	mailer2 = Mailer(login_, password_)
	while True:
		print("background_jobs")
		tz = pytz.timezone('Asia/Kolkata')
		kolkata_now = datetime.now(tz)
		t = int(kolkata_now.strftime('%H%M'))
		print(t)
		for i in db.search(where('type') == 'notification'):
			if 0 <= t - i['time'] < 10:
				print('Sending notifications')
				output = extractPrice(i['source'], i['link'])
				mailer2.sendMail(i['email'], "Notification",
				 '''<h3><a href="%s">%s</a></h3><br>The price at this moment is %s'''%(i['link'],i['name'], str(output)))
		time.sleep(600)

def background_jobs2():
	while True:

		time.sleep(60)

t1 = threading.Thread(target = background_jobs)
t1.start()

from app import routes

