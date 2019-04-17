import sys
import html2text
import sys
import re

def convertLinks(source, link):
	if source == "Amazon.in":
		try:
			newlink = link.split('/')
			ind = newlink.index('dp')
			product_id = newlink[ind+1]
		except:
			newlink = link.split('%2F')
			ind = newlink.index('dp')
			product_id = newlink[ind+1]
		link = "https://www.amazon.in/dp/" + product_id +"/"
	elif source == "Flipkart":
		link = link.split('/')[-1]
		link = link.split('?')[-1]
		link = link.split('&')
		for i in link:
			if i[:3] == "pid":
				pid = i
				break

		link = "https://www.flipkart.com/p/p/p?" + pid
		link = '\\/'.join(link.split('/'))
	elif source == "SnapDeal":
		link = link.split('#')[0]


	print(link)
	return link