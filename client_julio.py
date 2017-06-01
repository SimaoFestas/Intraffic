import requests

ip = 'http://localhost:8080/'
s=requests.Session()

while(True):
	x=input('status=')
	r=s.get(ip, params={'delete_pos':'a','info':'ultrapassagem','status':x})
	print(r.text)
	

