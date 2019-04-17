from flask import Flask
import time
from datetime import datetime, timezone
import pytz
from tinydb import TinyDB, where
from scrapers import extractPrice
from mailer import Mailer
from credentials import login_, password_, secret_key
import threading
import calendar

db = TinyDB('database.json')
db2 = TinyDB('history.json')
initial_time = 0
if not db2.contains(where('initial_time')):
	start_secs = calendar.timegm(time.gmtime())
	db2.insert({'initial_time': start_secs})
	initial_time = start_secs
else:
	initial_time = db2.search(where('initial_time'))[0]['initial_time']


app = Flask(__name__)
app.secret_key = secret_key

def background_jobs():
	mailer2 = Mailer(login_, password_)
	while True:
		db = TinyDB('database.json')
		print("background_jobs")
		tz = pytz.timezone('Asia/Kolkata')
		kolkata_now = datetime.now(tz)
		t = int(kolkata_now.strftime('%H%M'))
		print(t)
		for i in db.search(where('type') == 'notification'):
			if 0 <= t - i['time'] < 10:
				print(i)
				print('Sending notifications')
				output = extractPrice(i['source'], i['link'])
				print('Initializing mailer')
				mailer2.sendMail(i['email'], "Notification",
				 '''<h3><a href="%s">%s</a></h3><br>The price at this moment is &#8377;%s'''%(i['link'],i['name'], str(output)))
		time.sleep(600)

def background_jobs2():
	while True:
		print("background_jobs2")
		db1 = TinyDB('currently_recording.json')
		db2 = TinyDB('history.json')
		products = db1.all()
		current_time = calendar.timegm(time.gmtime())
		time_diff = current_time - initial_time
		for i in products:
			price = extractPrice(i['source'], i['link'])
			db2.insert({"name": i["name"], "source": i["source"], "link": i["link"], "price": price, "time": time_diff})
		time.sleep(60)

t1 = threading.Thread(target = background_jobs)
t1.start()
t2 = threading.Thread(target = background_jobs2)
t2.start()

from app import routes
