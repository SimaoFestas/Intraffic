import requests
import random
import json
import sys
import math
s = requests.Session()

# Google Maps Api Version
# GEOCODE KEY AIzaSyDyCjenIgBZ60k0FVF8NMhC8MdVUxkN3Nc
# GEOLOCATE KEY AIzaSyD8SzhhMB3JIcewYVh1MCnFyyJ3I873dsc
# DISTANCE KEY AIzaSyDhhQFCBvPs_HAVkV0ttjhuqnTzHgHza0A

def generate_random_data(lat, lon, num_rows):
	#Get random coordinates near lat and lon
    for _ in range(num_rows):
        dec_lat = random.random()/100
        dec_lon = random.random()/100
        return lat+dec_lon,lon+dec_lat 

def geolocation():
	# Get device location
	street_name = '---'
	city = '---'
	district = '---'
	country = '---'
	latitude = '---'
	longitude = '---'
	accuracy = '---'
	error = '0'
 
	geolocation = s.post('https://www.googleapis.com/geolocation/v1/geolocate?homeMobileCountryCode=351&homeMobileNetworkCode=06&radioType=gsm&carrier=MEO&considerIp=false&key=AIzaSyD8SzhhMB3JIcewYVh1MCnFyyJ3I873dsc')
	#Geolocation api key  AIzaSyD8SzhhMB3JIcewYVh1MCnFyyJ3I873dsc

	latitude = geolocation.json()['location']['lat']
	longitude = geolocation.json()['location']['lng']
	accuracy = geolocation.json()['accuracy']
	
	#get street
	url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key=AIzaSyDyCjenIgBZ60k0FVF8NMhC8MdVUxkN3Nc'.format(latitude=latitude,longitude=longitude)
	street = s.get(url) 
	status = street.json()['status']

	if(status!='OK'):
		#print('An error as occured! Please try again!')
		return	street_name,city,district,country,latitude,longitude,accuracy,error

	r = street.json()['results'] 
	street_name = r[0]['formatted_address']
	city = r[0]['address_components'][1]['long_name']
	district = r[0]['address_components'][2]['long_name']
	country = r[0]['address_components'][3]['long_name']
	
	return street_name,city,district,country,latitude,longitude,accuracy,error

def geolocation_fake_gps(lati,longi):
	# Generate random locations near ...

	street_name = '---'
	city = '---'
	district = '---'
	country = '---'
	latitude = '---'
	longitude = '---'
	fake_accuracy = '---'
	error = '0'

	url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key=AIzaSyDyCjenIgBZ60k0FVF8NMhC8MdVUxkN3Nc'.format(latitude=lati,longitude=longi)
	street = s.get(url) 

	status = street.json()['status']
	r = street.json()['results'] 
	if(status=='ZERO_RESULTS'):
		#print('ZERO_RESULTS')		
		error='1'
		return street_name,city,district,country,latitude,longitude,fake_accuracy,error

	if(status!='OK'):
		#print('An error as occured! Please try again!')
		error='1'
		return street_name,city,district,country,latitude,longitude,fake_accuracy,error
	
	fake_accuracy = 10
	street_name = r[0]['formatted_address'] # Address

	scountry = street_name.split(', ')
	country = scountry[len(scountry)-1]

	t = len(r[0]['address_components']) #Array length

	if t == 10:
		city = r[0]['address_components'][2]['long_name']
		district = r[0]['address_components'][5]['long_name']
	if t == 9:
		city = r[0]['address_components'][2]['long_name']
		district = r[0]['address_components'][5]['long_name']
		#country = r[0]['address_components'][5]['long_name']
	if t == 8:
		city = r[0]['address_components'][2]['long_name']
		district = r[0]['address_components'][4]['long_name']
	if t == 7:
		city = r[0]['address_components'][2]['long_name']
		district = r[0]['address_components'][3]['long_name']
	if t == 6:
		city = r[0]['address_components'][1]['long_name'] 
		district = r[0]['address_components'][3]['long_name']

	if t == 5:
		city = r[0]['address_components'][1]['long_name'] 
		district = r[0]['address_components'][2]['long_name']
	if t == 4:
		city = r[0]['address_components'][1]['long_name'] 
		district = r[0]['address_components'][2]['long_name']
	if t == 3:
		#Not tested
		city = r[0]['address_components'][1]['long_name'] 
	
	return street_name,city,district,country,latitude,longitude,fake_accuracy,error
	

def distance(latitude_point1,longitude_point1,latitude_point2,longitude_point2):
	# Distance betewen two locations 
	# DISTANCE KEY AIzaSyDhhQFCBvPs_HAVkV0ttjhuqnTzHgHza0A

	error = '0'
	distance_meters = 0

	dist = s.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=metricl&origins={latitude},{longitude}&destinations={latitude_point2},{longitude_point2}&key=AIzaSyDhhQFCBvPs_HAVkV0ttjhuqnTzHgHza0A'.format(latitude=latitude_point1,longitude=longitude_point1,latitude_point2=latitude_point2,longitude_point2=longitude_point2))
	status = dist.json()['status']

	if(status != 'OK'):
		error = '1'
		print('An error as occured! Please try again!')
		return distance_meters,error
	distance_meters = dist.json()['rows'][0]['elements'][0]['distance']['value']

	return distance_meters,error


