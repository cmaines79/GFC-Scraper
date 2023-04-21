import httpx
from selectolax.parser import HTMLParser

def get_je_designs():
	# local variables
	parsed_urls = []
	listings = []

	# get request for the parsed_urls from the landing page for all of the GFC Accessories
	r = httpx.get('https://jedesignandfabrication.ecwid.com/Go-Fast-Camper-Accessories-c113909263')

	# if else to ensure proper communication
	if(r.status_code == 200):

		# parsing data
		data = HTMLParser(r.text)

		# finding all fo the product title A tags so we can get the required link to the actual product
		atags = data.css('a.grid-product__title')

		for tag	 in atags:
			# find the trademark and replace it with a '%'
			url = tag.attrs['href']
			tm = url.find("-") -1
			# url = url[0:tm] + "%" + url[tm + 1:]
			url = url[0:tm] + url[tm + 1:]
			url = url.replace('tm', '')
			
			parsed_urls.append(url)
	else:
		print('Error parsing the home page for product links.  Error: ' + str(r.status_code))	
	
	# get requests for the individual products so we can get the info we need
	for url in parsed_urls:
		r = httpx.get(url)
		
		# a little security
		if(r.status_code == 200):
			# parse the get request
			data = HTMLParser(r.text)

			# geting the accessory title
			title = data.css_first('h1.product-details__product-title.ec-header-h3').text()

			# picture
			try:
				picture = data.css_first('img.details-gallery__picture').attrs['src']
			except:
				picture = data.css_first('div.logo > img').attrs['src']
	
			# price
			price = data.css_first('span.details-product-price__value.ec-price-item.notranslate').text()
			
			# description
			description = data.css_first('div#productDescription > div > p:nth-child(2').text()
			
			# build the list
			new_item = {
				"manufacturer" : 'JE Design and Fabrication',
				"Title" : title,
				"picture" : picture,
				"price" : price,
				"description" : description,
				"link" : url
			}
			# add list to dictionary
			listings.append(new_item)

		else:
			print('Error parsing the product pages.  Error: ' + r.status_code)	

def get_gfc_description(url, base_url):
	print(base_url + url)
	
	try:
		r = httpx.get(base_url + url)
	except:
		print("error getting description")

	if(r.status_code == 200):
		data = HTMLParser(r.text)
		#STUCK HERE!!!!
	else:
		return "Error parsing descrption"
			
def get_gfc():
	# local variables
	base_url = 'https://gofastcampers.com'
	gfc_listings = []
	
	try:
		r = httpx.get('https://gofastcampers.com/pages/gfc-accessories')
	except:
		print("Error wit get request")
	
	if(r.status_code == 200):
		# parse the data
		data = HTMLParser(r.text)

		# title
		title = data.css('div.pf-c > div > div > form > div > div > div > h3')

		# picture
		picture = data.css('div.pf-slide-main-media > img')
		
		# price
		price = data.css('div.pf-c > div > div > form > div > div > div > div:nth-child(3)')		

		#source url
		url = data.css('div.pf-main-media')

		#loop to get all of the produts into a dictionary
		i = 0

		while i < len(title):

			# build the list
			new_item = {
				"manufacturer" : 'JE Design and Fabrication',
				"Title" : title[i].text(),
				"picture" : picture[i].attrs['src'],
				"price" : price[i].text(),
				"description" : get_gfc_description(url[i].attrs['data-href'], base_url),
				"link" : url[i].attrs['data-href']
			}
			
			i += 1
			gfc_listings.append(new_item)
		
	else:
		print('Error parsing the main page.  Error: ' + r.status_code)

if __name__ == '__main__':
	# get_je_designs()
	get_gfc()

"""
Targeting GFC Accessory sites to see what's available and at what cost

Targeted Sites:
[] GFC: https://gofastcampers.com/collections/accessories
[X] JE Designs: https://jedesignandfabrication.ecwid.com/Go-Fast-Camper-Accessories-c113909263

"""