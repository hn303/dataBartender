---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Tutorial for collecting POIs through Google Places API"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-10-05T21:04:40+01:00
lastmod: 2019-10-05T21:04:40+01:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

## Step:
-	Get API from Google Cloud Platform
-	Google Places API
-	Create Fishnet
-	Create Python script 

## 1.	Get API from Google Cloud Platform
- Google Cloud Console
- Create a new project
- Choose APIs&Services/Library
- Enable Places API
- Create credentials (choose API key)
- **Set the restrictions**


## 2.	Google Search for Places API
Document for Google Places API can be found here.
Google Places APIs allow users to query for place information on a variety of categories (See list below). There are two ways to search for places: proximity and text string. The APIs are **Nearby Search requests** and **Text Search requests**.
**Nearby Search requests** allows to search for places within a specific area through supplying keywords or specifying the type of place.

A Nearby Search request is an HTTP URL of the following form:
https://maps.googleapis.com/maps/api/place/nearbysearch/output?parameters
where output may be either of the following values:
-	json indicates output in JavaScript Object Notation(JSON)
-	xml indicates output as XML

All parameters are separated using the ampersand (&) character

Required parameters
-	key — Your application's API key. This key identifies your application. See Get a key for more information.
-	location — The latitude/longitude around which to retrieve place information. This must be specified as latitude,longitude.
-	radius — Defines the distance (in meters) within which to return place results. The maximum allowed radius is `50 000 meters`. Note that radius must not be included if rankby=distance (described under Optional parameters below) is specified.
-	If rankby=distance (described under Optional parameters below) is specified, then one or more of keyword, name, or type is required.

Optional parameters
-	type — Restricts the results to places matching the specified type. Only one type may be specified
-	pagetoken — Returns the next 20 results from a previously run search. Setting a pagetoken parameter will execute a search with the same parameters used previously — all parameters other than pagetoken will be ignored.

Few key things about Nearby Search Request:
-	Maximum places per day from one account is 150000 POIs (according to second reference)
-	Result returned from Google are up to 20 each page. 
-	When the number of result is more than 20, next_page_token will be given in the former page 



## 3.	Google Place Details API
Place details: to get the complete details we have to use another API endpoint.
There is 3 categories for the fields parameter:

**Basic**:  `address_component`, `adr_address`, `alt_id`, `formatted_address`, `geometry`, `icon`, `id`, `name`, `permanently_closed`, `photo`, `place_id`, `plus_code`, `scope`, `type`, `url`, `utc_offset`, `vicinity`

**Contact**:  `formatted_phone_number`, `international_phone_number`, `opening_hours`, `website` 

**Atmosphere**:  `price_level`, `rating`, `review`


## 4.	Create fishnet on ArcGIS
output the point shapefile of fishnet. Take London for example, the coordinates of London center is 


```python
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
    api = GooglePlaces("YOUR KEY") #here is my API key
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
```
## Reference:
- Tutorial from [Gotrained Python Tutorials](https://python.gotrained.com/google-places-api-extracting-location-data-reviews/)
- Tutorial from [Jianshu](https://www.jianshu.com/p/76f058d3373f)