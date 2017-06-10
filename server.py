import random #import module random
import string #import module string
import sqlite3 #import module sqlite3
import cherrypy #import module cherrypy
import json #import module json
from datetime import datetime #import module datetime
import globalultrapassar
@cherrypy.expose
class StringGeneratorWebService(object):
	@cherrypy.tools.accept(media='text/plain')

	def GET(self, info,delete_pos='',id='',alerts='',street='',city='', district='', country='', precision='', latitude='',longitude='',ddatetime_start='',ddatetime_end='',status=''): #function get
		conn = sqlite3.connect('intraffic_database.db')  #connection to represent the database
		c=conn.cursor()
		if info == 'getall':
			x = c.execute("select * from Datalog where status LIKE ?", ('unsolved',)).fetchall()  #returns all "unsolved" alerts from the data base
			return json.dumps(x)
		elif info == 'getid':
			x = c.execute("select * from Datalog where Id=:x and status=:y",{"x":id,"y":status}).fetchall() #returns all alerts in data base that were made by this specific id
			return json.dumps(x)
		elif info == 'getlocal':
			x = c.execute("select * from Datalog where city=:x and country=:y and status=:z",{"x":city,"y":country,"z":status}).fetchall() # returns all alerts in this specific location
			return json.dumps(x)
		elif info == 'getalert':
			x = c.execute("select * from Datalog where alerts LIKE ?", (alerts,)).fetchall()  # returns all alerts, from a specific type of alert
			return json.dumps(x)
		elif info == 'delete' :
			ddatetime_end=str(datetime.now())
			x = c.execute("update Datalog set ddatetime_end=:x where AlertNr=:y and Id=:z",{"x":ddatetime_end,"y":delete_pos,"z":id})
			x = c.execute("update Datalog set status=:x where AlertNr=:y and Id=:z",{"x":'solved',"y":delete_pos,"z":id}) # updates status from "unsolved" to "solved", according to a input id
		#return alerts unsolved

		
		elif info=='ultrapassagem':
			if(status=='nao'):
				#não é possivel ultrapassar
				globalultrapassar.ultrapassar='nao'
			if(status=='sim'):
				globalultrapassar.ultrapassar='sim'
			if(status=='sem'):
				globalultrapassar.ultrapassar='sem'
			
			return globalultrapassar.ultrapassar
		elif info=='pedido':
			if(status=='sim'):
				globalultrapassar.pedido='sim'
			if(status=='nao'):
				globalultrapassar.pedido='nao'
			return globalultrapassar.pedido
		#http://localhost:8080/?&info=site		
		elif info == 'site':		# API 
			x = c.execute("select * from Datalog where status LIKE ?", ('unsolved',)).fetchall() # returns all "unsolved" alerts
			a=json.dumps(x)
			f=open("datalog.txt","w")
			f.write(a)
			f.close												# copies all alerts to a txt file
			return a											# returns json 
		else:
			x = c.execute("select * from Datalog")
			
		conn.commit()  # save (commit) the changes


	def POST(self,id,alerts,street,city,district,country,precision,latitude,longitude,ddatetime,status):	#function post
		conn = sqlite3.connect('intraffic_database.db')	#connection to represent the database
		c = conn.cursor()
		x = c.execute("select * from Datalog where id=:x and alerts=:y and status=:z",{"x": id,"y":alerts,"z":status}).fetchall()
		ddatetime_start = ddatetime
		ddatetime_end ='---'
		status = 'unsolved'
		c.execute("insert into Datalog (Id,alerts,street,city,district,country,precision,latitude,longitude,ddatetime_start,ddatetime_end,status) Values(?,?,?,?,?,?,?,?,?,?,?,?)",(id,alerts,street,city,district,country,precision,latitude,longitude,ddatetime_start,ddatetime_end,status))		

		'''	
		if json.dumps(x) == '[]':			# if its empty, post new alert with "unsolved" status
			ddatetime_start = ddatetime
			ddatetime_end = '---'
			status = 'unsolved' 
			c.execute("insert into Datalog (Id,alerts,street,city,district,country,precision,latitude,longitude,ddatetime_start,ddatetime_end,status) Values(?,?,?,?,?,?,?,?,?,?,?,?)",(id,alerts,street,city,district,country,precision,latitude,longitude,ddatetime_start,ddatetime_end,status))
			# stores information in data base
		else:
			ddatetime_end = ddatetime	#if its already stored an alert it changes his "status to "solved"
			string = json.dumps(x)
			s = string.split(', ')	
			s2 = s[0].split('[')
			delete_pos = s2[len(s2)-1]
			x = c.execute("update Datalog set ddatetime_end=:x where id=:y and alerts=:z",{"x":ddatetime_end,"y":id,"z":alerts})
			x = c.execute("update Datalog set status='solved' where AlertNr=?",(delete_pos,))
			#update of database, and stores time of update in the database
		'''
		conn.commit()	# save (commit) the changes


if __name__ == '__main__':
    conf = { 
    'global' : {
        'server.socket_host' : '0.0.0.0',
        'server.socket_port' : 5000,
        'server.thread_pool' : 8       #Configuration of port and ip of network
        },
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }

 
    cherrypy.quickstart(StringGeneratorWebService(), '/', conf)
