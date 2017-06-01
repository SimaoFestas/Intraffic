import requests

ip = 'http://localhost:8080/'
s=requests.Session()

while(True):
	x=input('resultado')
	r=s.get(ip, params={'delete_pos':'a','info':'ultrapassagem'})
	print(r.text)
	

