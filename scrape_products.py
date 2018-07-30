try:
	from time import sleep
	from selenium import webdriver 
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.common.by import By 
	from selenium.webdriver.firefox.options import Options
	from selenium.webdriver.support.ui import WebDriverWait 
	from selenium.webdriver.support import expected_conditions as EC 
	from selenium.common.exceptions import TimeoutException
	from tinydb import TinyDB, Query

	import json
	import time
	import pprint
	import re
	import urllib.request
	import pickle

	#    ------- Initialise database --------
	products_db = TinyDB('products.json')
	product = Query()
	#    ------------------------------------

	#    ---------------Regex----------------
	page_data = re.compile('<script \S+ id=\"is_script\">\n\twindow\.__INITIAL_STATE__ = ([\s\S]*?)\n</script>')
	#    ------------------------------------


	####
	# Defining a product structure as :
	# Review = {
	#	'id' : 'Some kind of ID'
	#	'item_id' : 'Another kind of ID', 
	# 	'listing_id': 'Yet another kind of ID', 
	#	'name' : 'Product Name', 
	# 	'subtitle' : Some weird thing but letting it be,
	#	'rating':{
	#           "type" : "RatingValue",
	#           "average" : 4.3,
	#           "base" : 5,
	#           "breakup" : [43, 23, 56, 267, 513],
	#           "count" : 902,
	#           "histogramBaseCount" : 513,
	#           "reviewCount" : 176
	# 	},
	# 	'link': Link to product,
	# 	'brand': Brand name,
	#	'price': Price,
	#	'flipkart_assured': true/false about flipkart assured on that product, 
	#	'category': analytics category
	# }
	#
	# Out of all the various kinds of ID, we will use `id` for identification
	#
	####

	startURL = 'https://www.flipkart.com/washing-machines/pr?sid=j9e,abm,8qx&otracker=categorytree'
	options = Options()
	options.add_argument("--headless")
	browser = webdriver.Firefox(firefox_options=options)
	browser.get(startURL)
	while(1):
		contents = urllib.request.urlopen(startURL).read().decode('utf8')
		t = page_data.findall(str(contents))
		page_json = json.loads(t[0][:-1])
		for slot in page_json['pageDataV4']['page']['data']['10003']:
			if slot['widget']['type'] == 'PRODUCT_SUMMARY':
				info_dict = slot['widget']['data']['products'][0]['productInfo']['value']
				product_x = {}
				product_x['id'] = info_dict['id']
				product_x['item_id'] = info_dict['itemId']
				product_x['listing_id'] = info_dict['listingId']
				product_x['name'] = info_dict['titles']['title']
				product_x['subtitle'] = info_dict['titles']['subtitle']
				product_x['rating'] = info_dict['rating']
				product_x['link'] = info_dict['smartUrl']
				product_x['brand'] = info_dict['productBrand']
				product_x['flipkart_assured'] = info_dict['flags']['enableFlipkartAdvantage']
				product_x['price'] = info_dict['pricing']['mrp']['value']
				product_x['category'] = info_dict['analyticsData']['category']
				if products_db.search(product['id'].exists()) and products_db.search(product['id'] == product_x['id']):
					print(product_x['id'],'already exists')
				else:
					products_db.insert(product_x)
					print(product_x['id'],'newly added')
		try:
			btn = browser.find_element_by_xpath("//span[text()='Next']")
			btn.click()
			startURL = browser.current_url
		except Exception as e:
			print(e)
			print('URL : ', startURL)
			break
	browser.close()

except Exception as e:
	print(e)
	print(str(e))
	browser.close()
