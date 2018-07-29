from time import sleep
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time
from tinydb import TinyDB, Query
import pprint
#    ------- Initialise database --------
reviews_db = TinyDB('reviews.json')
review = Query()
#    ------------------------------------

####
# Defining a review structure as :
# Review = {
#	'id' : 'Review ID'
#	'review_url' : 'Review URL', 
# 	'author_name': 'Name of author', 
#	'p_id' : 'Product ID', 
#	'date' : 'Date posted', 
#	'verified_purchase': 'True means verified, False otherwise', 
#	'rating' : 'Rating'
#	'title' : 'Review title', 
#   'text': 'Review text', 
#	'upvotes' : 'Number of upvotes',
#	'downvotes' : 'Number of downvotes',
#	'exists': 'True means review still present, False otherwise' 
# }
#
####

products = ['https://www.flipkart.com/moto-e4-plus-iron-gray-32-gb/p/itmexzbwxp3jstrg?pid=MOBEU9WRZHNDJANR&lid=LSTMOBEU9WRZHNDJANRXVMCW2&marketplace=FLIPKART&fm=neo/merchandising&iid=M_020cac4c-348b-4b74-a659-1c23dd66ffee_1_957E10L3KE_MC.MOBEU9WRZHNDJANR&ppt=CLP&ppn=CLP:motorola-mobile-phones-store&otracker=clp_pmu_v2_Moto+Mobiles+under+%E2%82%B910K_1_motor-categ-6b027_Moto+E4+Plus+%28Iron+Gray%2C+32+GB%29_motorola-mobile-phones-store_MOBEU9WRZHNDJANR_neo/merchandising_0&cid=MOBEU9WRZHNDJANR']

options = Options()
options.add_argument("--headless")
browser = webdriver.Firefox(firefox_options=options)

def get_processed_review(raw_review):
	try:
		raw_review.find_element_by_xpath(".//span[@class='_1EPkIx']").find_element_by_tag_name('span').click()
	except:
		pass
	result = {
		'exists':True,
	}

	r_url = raw_review.find_element_by_xpath(".//div[@class='SbFGpY']").find_element_by_tag_name('a').get_attribute('href')
	result['id'] = r_url[r_url.rfind('/')+1:]
	result['review_url'] = r_url

	rating = raw_review.find_element_by_xpath(".//div[contains(@class, 'hGSR34') and contains(@class, 'E_uFuv')]").text
	result['rating'] = int(rating[0])
	
	result['title'] = raw_review.find_element_by_xpath(".//p[@class='_2xg6Ul']").text

	result['author_name'] = raw_review.find_element_by_xpath(".//p[@class='_3LYOAd _3sxSiS']").text

	try:
		raw_review.find_element_by_xpath(".//p[@class='_19inI8']")
		result['verified_purchase'] = True
	except:
		result['verified_purchase'] = False

	result['upvotes'] = raw_review.find_elements_by_xpath(".//span[@class='_1_BQL8']")[0].text
	result['downvotes'] = raw_review.find_elements_by_xpath(".//span[@class='_1_BQL8']")[1].text
	
	result['text'] = raw_review.find_element_by_xpath(".//div[@class='qwjRop']").find_element_by_tag_name('div').find_element_by_tag_name('div').text

	date = raw_review.find_element_by_xpath(".//p[@class='_3LYOAd']").text
	result['date'] = time.strptime(date, '%d %b, %Y')
	
	return result


for product_link in products:
	pageNumber = 1
	browser.get( product_link )
	try:
		browser.find_element_by_xpath('//div[@class="swINJg _3nrCtb"]').click()
	except:
		continue

	reviews_processed = 0
	cur_url = browser.current_url
	print("Product: ",cur_url[25:cur_url.find('/',26)])
	sleep(1)
	while 1:
		raw_reviews = browser.find_elements_by_xpath( '//div[@class="row _3wYu6I _3BRC7L"]/div' )

		print ("Found",len(raw_reviews),"on page.")
		if len(raw_reviews) == 0:
			break
		else:
			raw_reviews.pop()
		for raw_review in raw_reviews:
			processed_review = get_processed_review(raw_review)
			processed_review['p_id'] = browser.current_url[browser.current_url.find("pid=")+4:]
			if reviews_db.search(review.id.exists()) and reviews_db.search(review.id == processed_review['id']):
				pass
			else:
				reviews_db.insert(processed_review)

		try:
			browser.find_element_by_xpath('//div[@class="_2kUstJ"]/a/span[contains(text(),"Next")]').click()
		except:
			break

browser.close()
