import sys
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
import html2text
import threading
from convertLinks import convertLinks

	
class scraper(object):
	def __init__(self, productName):
		self.productName = re.sub(r"[,.;@#?!&$()-]+\ *", " ", productName)
		self.options = Options()
		self.options.headless = True
		browser = webdriver.Firefox(options = self.options)
		self.products = []
		t1 = threading.Thread(target = scraper.amazonScraper, args = (self, ))
		t2 = threading.Thread(target = scraper.paytmMallScraper, args = (self, ))
		t3 = threading.Thread(target = scraper.snapdealScraper, args = (self, ))
		t4 = threading.Thread(target = scraper.flipkartScraper, args = (self, ))
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()
		self.products = self.flipkart + self.amazon + self.paytmMall + self.snapdeal 
		self.sortByPriceAscending()
		print("Scraper initialized and prices fetched")

	def flipkartScraper(self):
		browser = webdriver.Firefox(options = self.options)
		self.flipkartURL = "https://www.flipkart.com/search?q="
		self.flipkartURL += '+'.join(self.productName.split())

		print("Searching URL:", self.flipkartURL)
		browser.get(self.flipkartURL)
		flag=0
		names = browser.find_elements_by_css_selector("._3wU53n")
		links = browser.find_elements_by_css_selector("._31qSD5")
		prices = browser.find_elements_by_css_selector("._2rQ-NK")
		images= browser.find_elements_by_css_selector("._1Nyybr._30XEf0")
		if(len(names)==0):
			names = browser.find_elements_by_css_selector("._3liAhj ._2cLu-l")
			links = browser.find_elements_by_css_selector("._3liAhj .Zhf2z-")
			prices = browser.find_elements_by_css_selector("._3liAhj ._1vC4OE")
			images = browser.find_elements_by_css_selector("._1Nyybr._30XEf0")
			flag=1

		if(len(names)==0):
			names = browser.find_elements_by_css_selector("._2mylT6")
			links = browser.find_elements_by_css_selector("._3dqZjq")
			prices = browser.find_elements_by_css_selector("._3O0U0u ._1vC4OE")
			images = browser.find_elements_by_css_selector("._3togXc")
			flag=0
		price=[];
		
		for i in range(len(prices)):
			price.append(prices[i].text)
			price[i]=price[i][1:]
			#print(price[i]);
			#img_src=find(links[i].get_attribute("href"));
			#img.append(img_src);
		minimum = min(len(names), len(links), len(prices), len(images))
		flipkart=[];
		for i in range(min(10, minimum)):
			if(flag==0):
				flipkart.append({
						"name": names[i].text,
						"price": float(html2text.html2text(''.join(price[i].split(',')))),
						"link": convertLinks("Flipkart", links[i].get_attribute('href')),
						"image": images[i].get_attribute("src"),
						"source": "Flipkart"})
			elif(flag==1):
				flipkart.append({
						"name": names[i].get_attribute("title"),
						"price": float(html2text.html2text(''.join(price[i].split(',')))),
						"link": links[i].get_attribute('href'),
						"image": images[i].get_attribute("src"),
						"source": "Flipkart"})
				
		self.flipkart = flipkart
		browser.quit()

	def amazonScraper(self):
		browser = webdriver.Firefox(options = self.options)
		self.amazonURL = "https://amazon.in/s/?field-keywords="
		self.amazonURL += '+'.join(self.productName.split())

		print("Searching URL:", self.amazonURL)
		browser.get(self.amazonURL)

		names = browser.find_elements_by_css_selector(".s-result-item h5 a span")
		links = browser.find_elements_by_css_selector(".s-result-item h5 a")
		prices = browser.find_elements_by_xpath('//span[@class="a-price"][@data-a-size="l"]/span[@class="a-offscreen"]')
		images = browser.find_elements_by_css_selector(".s-result-item img")


		print(len(names), len(links), len(prices), len(images))
		minimum = min(len(names), len(links), len(prices), len(images))
		amazon = []

		for i in range(min(10,minimum)):
			print(links[i].get_attribute('href'))
			amazon.append({
						"name": names[i].get_attribute("innerHTML"),
						"price": float(html2text.html2text(''.join(prices[i].get_attribute("innerHTML").split(',')))[1:]),
						"link": convertLinks("Amazon.in", links[i].get_attribute('href')),
						"image": images[i].get_attribute('src'),
						"source": "Amazon.in"})
		browser.quit()
		self.amazon = amazon
	

	def paytmMallScraper(self):
		browser = webdriver.Firefox(options = self.options)
		self.paytmMallURL = "https://paytmmall.com/shop/search?q="
		self.paytmMallURL += ' '.join(self.productName.split())
		self.paytmMallURL += '&from=organic'

		print("Searching URL:", self.paytmMallURL)
		browser.get(self.paytmMallURL)

		items = browser.find_elements_by_css_selector('div._2apC')
		prices = browser.find_elements_by_css_selector('div._1kMS span')
		links = browser.find_elements_by_css_selector('div._3WhJ')
		images = browser.find_elements_by_css_selector('div._3nWP')

		minimum = min(len(items), len(prices), len(links), len(images))

		paytmMall = []
		for i in range(min(10, minimum)):
			try:
				paytmMall.append({
						"name": items[i].get_attribute("innerHTML"),
						"price": float(html2text.html2text(''.join(prices[i].text.split(',')))),
						"link": convertLinks('PayTM Mall', links[i].find_element_by_tag_name('a').get_attribute('href')),
						"image": images[i].find_element_by_tag_name('img').get_attribute('src'),
						"source": "PayTM Mall"})
			except:
				continue
		browser.quit()
		self.paytmMall = paytmMall

	def snapdealScraper(self):
		browser = webdriver.Firefox(options = self.options)
		self.snapdealURL = "https://snapdeal.com/search?keyword="
		self.snapdealURL += '+'.join(self.productName.split())

		print("Searching URL:", self.snapdealURL)
		browser.get(self.snapdealURL)

		items = browser.find_elements_by_css_selector('.product-title')
		prices = browser.find_elements_by_css_selector('.product-price')
		links = browser.find_elements_by_css_selector('.dp-widget-link.noUdLine.hashAdded')
		images = browser.find_elements_by_css_selector('.product-image')

		snapdeal = []
		minimum = min(len(items), len(prices), len(links), len(images))
		for i in range(min(8, minimum)):
			try:
				snapdeal.append({
						"name": items[i].get_attribute("title"),
						"price": float(html2text.html2text(''.join(prices[i].get_attribute("display-price").split(',')))),
						"link": convertLinks('SnapDeal', links[2*i].get_attribute('href'))	,
						"image": images[2*i + 1].get_attribute('src'),
						"source": "SnapDeal"})
			except:
				continue
		
		browser.quit()
		self.snapdeal = snapdeal

	def sortByPriceAscending(self):
		for i in range(0,len(self.products)-1, 1):
			for j in range(0, len(self.products)-i-1, 1):
				if self.products[j]['price'] > self.products[j+1]['price']:
					self.products[j+1], self.products[j] = self.products[j], self.products[j+1]

	def __repr__(self):
		return str(self.products)


def extractPrice(store, link):
	options = Options()
	options.headless = True
	browser = webdriver.Firefox(options = options)
	browser.get(link)
	price = None
	if store == "Amazon.in":
		try:
			price = browser.find_element_by_css_selector("#priceblock_ourprice").text
		except:
			price = browser.find_element_by_css_selector(".a-declarative .a-section .a-color-price").text
		for i in price.split():
			try:
				price = float(i)
			except:
				continue
	elif store == "PayTM Mall":
		price = browser.find_element_by_css_selector("span._1V3w").text
	elif store == "SnapDeal":
		price = browser.find_element_by_css_selector(".payBlkBig").text
	elif store == "Flipkart":
		price = browser.find_element_by_css_selector("._1vC4OE._3qQ9m1").text[1:]

	browser.quit()

	return float(''.join(price.split(',')))