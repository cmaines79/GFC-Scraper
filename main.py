import httpx
# import time
from selectolax.parser import HTMLParser

def get_je_designs():
	# local variables
	# base_url = 'https://jedesignandfabrication.ecwid.com'
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
			url = url[0:tm] + "%" + url[tm + 1:]
			
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
			picture = data.css_first('div.details-gallery__image-wrapper-inner')
			# picture = picture.attrs['src']
			print(picture)
	
			# price
			# description
			# build the list
			new_item = {
				"manufacturer" : 'JE Design and Fabrication',
				"Title" : title,
				"picture" : '',
				"price" : '',
				"description" : '',
				"link" : url
			}
			# add list to dictionary
			listings.append(new_item)
			
			
		else:
			print('Error parsing the product pages.  Error: ' + r.status_code)	
	

if __name__ == '__main__':
	get_je_designs()

"""
Targeting GFC Accessory sites to see what's available and at what cost

Targeted Sites:
[] GFC: https://gofastcampers.com/collections/accessories
[] JE Designs: https://jedesignandfabrication.ecwid.com/Go-Fast-Camper-Accessories-c113909263

"""