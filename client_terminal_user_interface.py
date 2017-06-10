import requests # importing the Requests module
import random # importing the random module
import json # importing the json module 
from time import gmtime, strftime #from module time importing gmtime(Convert a time expressed in seconds to a struct_time, year,monyh, day, hour, minute, seconds) and strftime(Convert a tuple representing a time as returned by gmtime to a string as specified by the format argument)
from datetime import datetime #from datetime module importing datetime(A combination of a date and a time. Attributes: year, month, day, hour, minute, second, microsecond)
from location import * #from locaction_en importing every functions 

ip = 'http://localhost:5000/'  #ip = 'http://192.168.1.177:5000/'    #define ip and port
id = '12-NM-87' #define car/robot id
latitude_start = 40.629  # Aveiro
longitude_start = -8.653 # Aveiro

s = requests.Session() #creating a persistent session 

def post(alert): #function post
	car = id #copys car/robot id to variable car 	
	latitude,longitude = generate_random_data(latitude_start,longitude_start,1)	#gets latitude and longitude from function genera_random_data(*arguments*) from location_en.py
	street,city,district,country,lati,longi,fakeaccuracy,error = geolocation_fake_gps(latitude,longitude)#gets street,city,district,country,lati,longi,fakeaccuracy,error from geolocation_fake_gps(*arguments*) using latitude and longitude as arguments, from location_en.py
	if(error=='0'):
		status = 'unsolved' #if error=0, puts the status of new ialert as unsolved 
		ddatetime = str(datetime.now()) #gets the time that the new alert was posted 
		r = s.post(ip, params={'id': car,'alerts':alert,'street':street,'city': city,'district': district, 'country':country,'precision':fakeaccuracy,'latitude':latitude,'longitude':longitude,'ddatetime':ddatetime, 'status': status}) #gets all the information necessary to define the location of the alert
	else:
		print('An error as occured! Please try again!') #if error=1, prints a error message 
	
def get(info,delete_pos='',id='',alerts='',street='',city='', district='', country='', precision='', latitude='',longitude='',ddatetime_start='',ddatetime_end='',status=''): #Function get
	r = s.get(ip, params={'info': info,'delete_pos':delete_pos, 'id': id,'alerts':alerts,'street':street,'city': city, 'country':country,'precision':precision,'latitude':latitude,'longitude':longitude,'ddatetime_start':ddatetime_start,'ddatetime_end':ddatetime_end, 'status': status}) #gets params of the alert
	return r.text

def printInfo(text):
	if text == '[]': #if text as nothing
		print("No data")# prints the information that there is no data 
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

def get_id_ui(alert_status): #get information from id in session
	return get(info='getid',id=id,status=alert_status) #gets status of the alerts

def get_local_ui(): #get local allerts
	latitude,longitude = generate_random_data(latitude_start,longitude_start,1) 	#gets latitude and longitude from function genera_random_data(*arguments*) from location_en.py
	street,city,district,country,lati,longi,fakeaccuracy,error = geolocation_fake_gps(latitude,longitude) #gets street,city,district,country,lati,longi,fakeaccuracy,error from geolocation_fake_gps(*arguments*) using latitude and longitude as arguments, from location_en.py
	if(error=='0'):
		info = get(info='getlocal',city=city,country=country,status='unsolved') #if error = 0, gets unsolved alerts
	else:
		info = 'error'
		print('An error as occured! Please try again!')	#if erro = 1, prints information that an error as occured
	return info

def get_alert_ui(alerts): #gets all alerts
	return get(info='getalert',alerts=alerts)

def get_range_ui(range_km): #gets all occurrences in a range defined by the user
	#k=int(input('Range (in Km)')) #range
	latitude,longitude = generate_random_data(latitude_start,longitude_start,1) 	#gets latitude and longitude from function genera_random_data(*arguments*) from location_en.py
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

def post_ui(alert): #posts the alerts
	if alert == '1': #if alert = 1
		post('Accident') # post accident
	elif alert == '2': #else if alert = 2
		post('Failure') # post failure
	elif alert == '3': #else if alert = 3
		post('Road with poor condition/Signaling') # posrt Road with pooe condition/Signaling
	else: #else if alert != [1,2,3], 
		print('Invalid option! Alert not sent!') # print an error message

def delete_ui(alertnumb): #puts an unsolved alert in to a solved alert if the alert is solved
	# define status = 'solved'
	t = get(info='delete',delete_pos=alertnumb)	

def exit_ui(): # exits the interface
	#End connection
	s.close()
	


# Terminal- User Interface

while True:
	id = input('Enter the registration number of your vehicle: ')	#input car/robot id
	if len(id) == 8: #if len(id) == 8, define the various type of plates registrations 
		if (id[0:1].isupper() == True) and (id[2] == '-') and (id[3:4].isdigit() == True) and (id[5] == '-') and (id[6:7].isdigit() == True):
			break
		if (id[0:1].isdigit() == True) and (id[2] == '-') and (id[3:4].isdigit() == True) and (id[5] == '-') and (id[6:7].isupper() == True):
			break
		if (id[0:1].isdigit() == True) and (id[2] == '-') and (id[3:4].isupper() == True) and (id[5] == '-') and (id[6:7].isdigit() == True):
			break

while True:
	x = input('\n------------------------------|| INTRAFFIC ||------------------------------\n GET INFORMATION -> get \n POST -> post\n DELETE -> delete\n EXIT -> x\n->') # interface, now the client can choose what he wants to do
	if x=='get': #if x= get, goes to another Interface, the Interface with all the types of get funciton mentioned above
			g=input('\n Get All alerts online -> getall \n Get alerts that you have sent -> getid \n Get alerts on your location -> getlocal \n Get reports by alert that you want -> getalert \n Get alerts unsolved on a range of:_ _ -> getrange \n Command: ')
			if g == 'getall':

				t = get(info='getall') 
				printInfo(t)
			elif g == 'getid':
				p=input('Unsolved Alerts -> unsolved \n  Solved Alerts  -> solved ')
				t = get(info='getid',id=id,status=p)
				printInfo(t)
			elif g == 'getlocal':
				latitude,longitude = generate_random_data(500,-10,10) 	#gets latitude and longitude from function genera_random_data(*arguments*) from location_en.py
				street,city,district,country,lati,longi,fakeaccuracy,error = geolocation_fake_gps(latitude,longitude) #gets street,city,district,country,lati,longi,fakeaccuracy,error from geolocation_fake_gps(*arguments*) using latitude and longitude as arguments, from location_en.py
				print(city)
				if(error=='0'):
					t = get(info='getlocal',city=city,country=country,status='unsolved')
					printInfo(t)
				else:
					print('An errorr as occured! Please try again!')
					
			elif g == 'getalert':
				alerts = input("Alert:")
				t = get(info='getalert',alerts=alerts)
				printInfo(t)
			elif g=='getrange':
				k=int(input('Range (in Km):')) 
				latitude,longitude = generate_random_data(40.629,-8.653,1) 	#gets latitude and longitude from function genera_random_data(*arguments*) from location_en.py
				t= json.loads(get(info='getall'))
				
				lst = []
				
				for dst in t:
					d,error = distance(latitude,longitude,dst[8],dst[9])
					if(error=='0'):
						print(d)
						if d < k*1000: 
							lst += [dst,d]
					else:
						print('An errorr as occured! Please try again!')
					
				l = str([str(ls) for ls in lst])
				printInfo(l)
			else:
				pass
	elif x == 'delete': #if x= delete, gets all the alerts from the id that posted them and delete the one that is solved
			r = get(info='getid',id=id,status='unsolved')
			printInfo(r)
			alertnumb = input("Which alert do you wish to delete: ")
			t = get(info='delete',delete_pos=alertnumb)			
	elif x == 'post':# if x= post, goes to another interface that have the Alerts that the client can send
			alert = input("  Accident - 1\n  Failure - 2\n  Road with poor condition/Signaling - 3\n ->")
			if alert == '1':
				post('Accident')
			elif alert == '2':
				post('Failure')
			elif alert == '3':
				post('Road with poor condition/Signaling')
			else:
				print('Invalid option! Alert not sent!')
	elif x == 'x': #if x= x the client is offline. 
				s.close()
				break

print('Connection to the server has been lost')
