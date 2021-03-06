import requests
import random
import json
from time import gmtime, strftime
from datetime import datetime
from location import *


ip = 'http://localhost:5000/'    #define ip and port
id = '12-NM-87' #define car/robot id
latitude_start = 40.629  # Aveiro
longitude_start = -8.653 # Aveiro

s = requests.Session()
def post(alert):
	car = id
	latitude,longitude = generate_random_data(latitude_start,longitude_start,1)	
	street,city,district,country,lati,longi,fakeaccuracy,error = geolocation_fake_gps(latitude,longitude)
	if(error=='0'):
		status = 'unsolved'
		ddatetime = str(datetime.now())
		r = s.post(ip, params={'id': car,'alerts':alert,'street':street,'city': city,'district': district, 'country':country,'precision':fakeaccuracy,'latitude':latitude,'longitude':longitude,'ddatetime':ddatetime, 'status': status})
	else:
		print('An error as occured! Please try again!')
	
def get(info,delete_pos='',id='',alerts='',street='',city='', district='', country='', precision='', latitude='',longitude='',ddatetime_start='',ddatetime_end='',status=''):
	r = s.get(ip, params={'info': info,'delete_pos':delete_pos, 'id': id,'alerts':alerts,'street':street,'city': city, 'country':country,'precision':precision,'latitude':latitude,'longitude':longitude,'ddatetime_start':ddatetime_start,'ddatetime_end':ddatetime_end, 'status': status}) 
	return r.text

def printInfo(text):
	if text == '[]':
		print("No data")
	else:
		x = text.split('], [')
		if len(x) == 1:
			print('\n   ' + text)
		else:
			z = x[0].split('[[')
			print('\n   '+z[1])
			for n in range(1,len(x)):
				print('   '+x[n]) 


def get_all_ui():
	# Get all the information
	return get(info='getall')

def get_id_ui(alert_status):
	return get(info='getid',id=id,status=alert_status)

def get_local_ui():
	latitude,longitude = generate_random_data(latitude_start,longitude_start,1)
	street,city,district,country,lati,longi,fakeaccuracy,error = geolocalizacao_fake_gps(latitude,longitude)
	if(error=='0'):
		info = get(info='getlocal',city=city,country=country,status='unsolved')
	else:
		info = 'error'
		print('An error as occured! Please try again!')	
	return info

def get_alert_ui(alerts):
	return get(info='getalert',alerts=alerts)

def get_range_ui(range_km):
	#k=int(input('Range (in Km)')) #range
	latitude,longitude = generate_random_data(latitude_start,longitude_start,1) 
	t= json.loads(get(info='getall'))
			
	lst = []
				
	for dst in t:
		d,error = distance(latitude,longitude,dst[8],dst[9])
		if(error=='0'):
			print(d)
			if d < range_km*1000: 
				lst += [dst,d]
		else:
			print('An error as occured! Please try again!')
			
	info = str([str(ls) for ls in lst])
	return info

def post_ui(alert):
	if alert == '1':
		post('Accident')
	elif alert == '2':
		post('Failure')
	elif alert == '3':
		post('Road with poor condition/Signaling')
	else:
		print('Invalid option! Alert not sent!')

def delete_ui(alertnumb):
	# define status = 'solved'
	t = get(info='delete',delete_pos=alertnumb)	

def exit_ui():
	#End connection
	s.close()
	
