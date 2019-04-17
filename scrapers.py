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
		self.browser = webdriver.Firefox(options = self.options)
		self.products = [] 
		self.amazon = self.amazonScraper()
		self.paytmMall = self.paytmMallScraper()
		self.snapdeal = self.snapdealScraper()
		self.flipkart = self.flipkartScraper()
		self.products = self.flipkart + self.amazon + self.paytmMall + self.snapdeal 
		self.sortByPriceAscending()
		print("Scraper initialized and prices fetched")

	def flipkartScraper(self):
		self.flipkartURL = "https://www.flipkart.com/search?q="
		self.flipkartURL += '+'.join(self.productName.split())

		print("Searching URL:", self.flipkartURL)
		self.browser.get(self.flipkartURL)
		flag=0
		names = self.browser.find_elements_by_css_selector("._3wU53n")
		links = self.browser.find_elements_by_css_selector("._31qSD5")
		prices = self.browser.find_elements_by_css_selector("._2rQ-NK")
		images= self.browser.find_elements_by_css_selector("._1Nyybr._30XEf0")
		if(len(names)==0):
			names = self.browser.find_elements_by_css_selector("._3liAhj ._2cLu-l")
			links = self.browser.find_elements_by_css_selector("._3liAhj .Zhf2z-")
			prices = self.browser.find_elements_by_css_selector("._3liAhj ._1vC4OE")
			images = self.browser.find_elements_by_css_selector("._1Nyybr._30XEf0")
			flag=1

		if(len(names)==0):
			names = self.browser.find_elements_by_css_selector("._2mylT6")
			links = self.browser.find_elements_by_css_selector("._3dqZjq")
			prices = self.browser.find_elements_by_css_selector("._3O0U0u ._1vC4OE")
			images = self.browser.find_elements_by_css_selector("._3togXc")
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
				
			
		return flipkart

	def amazonScraper(self):
		self.amazonURL = "https://amazon.in/s/?field-keywords="
		self.amazonURL += '+'.join(self.productName.split())

		print("Searching URL:", self.amazonURL)
		self.browser.get(self.amazonURL)

		names = self.browser.find_elements_by_css_selector(".s-result-item h5 a span")
		links = self.browser.find_elements_by_css_selector(".s-result-item h5 a")
		prices = self.browser.find_elements_by_xpath('//span[@class="a-price"][@data-a-size="l"]/span[@class="a-offscreen"]')
		images = self.browser.find_elements_by_css_selector(".s-result-item img")


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
			
		return amazon
	

	def paytmMallScraper(self):
		self.paytmMallURL = "https://paytmmall.com/shop/search?q="
		self.paytmMallURL += ' '.join(self.productName.split())
		self.paytmMallURL += '&from=organic'

		print("Searching URL:", self.paytmMallURL)
		self.browser.get(self.paytmMallURL)

		items = self.browser.find_elements_by_css_selector('div._2apC')
		prices = self.browser.find_elements_by_css_selector('div._1kMS span')
		links = self.browser.find_elements_by_css_selector('div._3WhJ')
		images = self.browser.find_elements_by_css_selector('div._3nWP')

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
		return paytmMall

	def snapdealScraper(self):
		self.snapdealURL = "https://snapdeal.com/search?keyword="
		self.snapdealURL += '+'.join(self.productName.split())

		print("Searching URL:", self.snapdealURL)
		self.browser.get(self.snapdealURL)

		items = self.browser.find_elements_by_css_selector('.product-title')
		prices = self.browser.find_elements_by_css_selector('.product-price')
		links = self.browser.find_elements_by_css_selector('.dp-widget-link.noUdLine.hashAdded')
		images = self.browser.find_elements_by_css_selector('.product-image')

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
		
		return snapdeal

	def sortByPriceAscending(self):
		for i in range(0,len(self.products)-1, 1):
			for j in range(0, len(self.products)-i-1, 1):
				if self.products[j]['price'] > self.products[j+1]['price']:
					self.products[j+1], self.products[j] = self.products[j], self.products[j+1]

	def __repr__(self):
		return str(self.products)

	def __del__(self):
		print("Scraper object destroyed")
		self.browser.quit()


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
				price = float(price)
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