# Flipkart_Scraper
Flipkart Scraper  

## Run instructions

- Install selenium and a corresponding web-browser driver (prefer firefox gecko driver for the headless mode)  
- Install TinyDB (pip install tinydb)  

### For product reviews
Run the `scrape_flipkart_reviews.py` after adding links to all the products for which reviews are desired to be scraped [here](https://github.com/LCS2-IIITD/Flipkart_Scraper/blob/master/scrape_flipkart_reviews.py#L36).  

### For product information
Run the `scrape_products.py` after adding links to all the products that are required to be scraped [here](https://github.com/LCS2-IIITD/Flipkart_Scraper/blob/master/scrape_products.py#L56).  

## Scraped Data structure
All of this is scraped as a TinyDB object and stored in the corresponding file. Details about tiny db and related documentation can be read on [TinyDB's official documentation](https://tinydb.readthedocs.io/en/latest/).  

### Reviews
```
Review = {
  'id' : 'Review ID'
	'review_url' : 'Review URL', 
 	'author_name': 'Name of author', 
	'p_id' : 'Product ID', 
  'date' : 'Date posted', 
	'verified_purchase': 'True means verified, False otherwise', 
	'rating' : 'Rating'
	'title' : 'Review title', 
  'text': 'Review text', 
	'upvotes' : 'Number of upvotes',
	'downvotes' : 'Number of downvotes',
	'exists': 'True means review still present, False otherwise' 
}
```

### Products
```
Review = {
		'id' : 'Some kind of ID'
		'item_id' : 'Another kind of ID', 
	 	'listing_id': 'Yet another kind of ID', 
		'name' : 'Product Name', 
	 	'subtitle' : Some weird thing but letting it be,
		'rating':{
	           "type" : "RatingValue",
	           "average" : 4.3,
	           "base" : 5,
	           "breakup" : [43, 23, 56, 267, 513],
	           "count" : 902,
	           "histogramBaseCount" : 513,
	           "reviewCount" : 176
	 	},
	 	'link': Link to product,
	 	'brand': Brand name,
		'price': Price,
		'flipkart_assured': true/false about flipkart assured on that product, 
		'category': analytics category
}
```
