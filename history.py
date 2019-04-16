import io;
import base64
import matplotlib.pyplot as plt
import numpy as np
from tinydb import TinyDB, where
from sklearn.linear_model import LinearRegression

def get_history(link):
	# db1 = TinyDB('currently_recording.json')
	print("In get_history")
	print("Link: %s"%link)
	# if not db1.contains(where('link') == link):
	# 	return False
	db2 = TinyDB('history.json')
	history = db2.search(where('link') == link)
	print("history length: %d"%len(history))
	if len(history) < 10:
		return False
	return history

def build_plot(x = [1,2,3,4,5,6,7,8,9,10], y = [10,6,9,12,14,11,8,11,3,4]):

	img = io.BytesIO()
#	img1 = io.BytesIO()
	
	x = np.array(x).reshape(-1, 1)
	y = np.array(y).reshape(-1, 1)
	print(x)
	print(y)
	reg = LinearRegression().fit(x,y)
	x_pred = x[-1] - x[0] + np.array(x)
	x_pred = x_pred.reshape(-1, 1)
	print(x_pred)
	y_pred = reg.predict(x_pred)
	plt.figure()
	plt.plot(x, y, label = 'Recorded prices')
	plt.plot(x_pred, y_pred, label = 'Predict prices')
	plt.title("Price Graph")
	plt.xlabel("Time")
	plt.ylabel("Prices")
	plt.legend(loc = 'best')
	plt.grid(True)
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()
	source = "data:image/png;base64,{}".format(plot_url)
	return source