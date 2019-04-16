import io;
import base64
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

def build_plot(x, y):

	img = io.BytesIO()
	img1 = io.BytesIO()
	
	x = np.array([1,2,3,4,5,6,7,8,9,10]).reshape(-1, 1)
	y = np.array([10,6,9,12,14,11,8,11,3,4]).reshape(-1, 1)
	reg = LinearRegression().fit(x,y)
	x_pred=np.array([11,12,13,14,15,16,17,18,19,20]).reshape(-1, 1)
	y_pred=reg.predict(x_pred);
	plt.hist(x,weights=y);
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()
	plt.figure();
	plt.hist(x_pred,weights=y_pred)
	plt.savefig(img1, format='png')
	img1.seek(0)

	plot_url1 = base64.b64encode(img1.getvalue()).decode()

	return "data:image/png;base64,{}".format(plot_url),"data:image/png;base64,{}".format(plot_url1)

store=[];
store=build_plot()
print(store[0])
print()
print(store[1])