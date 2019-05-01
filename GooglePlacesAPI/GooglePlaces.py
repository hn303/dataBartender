#this is code for Google Places API
import requests # requests through url
import json
import time #to take a break

import xlwt
import xlrd

class GooglePlaces(object):
	def __int__(self, apikey):
		super(GooglePlcaes, self).__init__()
		self.apikey = apikey

	def search_places_by_coordinate(self, location, radius, types): # these are parameters for Google Places API
		endpoint_url = "htttp://maps.googleapis.com/maps/api/plcae/nearbysearch/json"
		places = [] #create a list to store all result from multiple pages
		params = {
		"location": location,
		"radius": radius,
		"types": types,
		"key": self.apikey
		}

		# count the number of requests
		count = 0
		count_worked = 0
		for i in range(nrows): #nrows refers to the number of subareas in the fishnet
			lat = table.cell_value(i+1,1) #table.cell
			lng = table.cell_value(i+1,2)
			location = str(lat)+","+str(lng)
			#location = "51.526329,-0.139214"
			res = requests.get(endpoint_url, params = params) #requests.get(url,paramters)
			results = json.loads(res.content) #res.content()
			places.extend(results['results'])
			time.sleep(2)
			while "next_page_token" in results:
				params['pagetoken'] = results['next_page_token']
				res = requests.get(endpoint_url, params = params)
				results = json.loads(res.content)
				places.extend(results['results'])
				time.sleep(2)
			count += 1
			if count >100: #based on the maximum requests per day,60*100=6000
				break
			else:
				continue
		return results
	# def get_place_details(self, place_id, fields):
	# 	endpoint_url = 'https://maps.googleapis.com/maps/api/place/details/json'
	# 	params = {
	# 	"placeid": place_id,
	# 	"fields": ",".join(fields),
	# 	"key":self.apiKey
	# 	}
	# 	res = requests.get(endpoint_url, params = params)
	# 	place_details = json.load(res.content)
	# 	return place_details

#read fishnet file
xlsxdata = xlrd.open_workbook(r'/Users/qxy/Desktop/fish_points500_label_wgs.xlsx') #读取fishnet生成的点文件
table = xlsxdata.sheet_by_name("points500_label_wgs")
nrows = table.nrows #表格总行数


if __name__ == '__main__':
    api = GooglePlaces("AIzaSyCtC4ewHjta76uqJ9qmGnOtnohXIHVxkns") #here is my API key
    places = api.search_places_by_coordinate(location, "100", "restaurant")
    fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']
    for place in places:
    	details = api.get_place_details(place['place_id'], fields)
    	try:#sometimes, the value for some field is empaty, so we need to use try
    		website = details['result']['website']
    	except KeyError:
    		website = ''
    	try:
        name = details['result']['name']
	    except KeyError:
	        name = ""
	 
	    try:
	        address = details['result']['formatted_address']
	    except KeyError:
	        address = ""
	 
	    try:
	        phone_number = details['result']['international_phone_number']
	    except KeyError:
	        phone_number = ""
	 
	    try:
	        reviews = details['result']['reviews']
	    except KeyError:
	        reviews = []


