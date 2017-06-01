import random
import string
import sqlite3
import cherrypy
import json
import globalultrapassar
    
@cherrypy.expose

class StringGeneratorWebService(object):
	@cherrypy.tools.accept(media='text/plain')

	def GET(self,delete_pos, info,id='',alerts='',street='',city='', district='', country='', precision='', latitude='',longitude='',ddatetime_start='',ddatetime_end='',status=''):
		
		conn = sqlite3.connect('database_v4_en.db')
		c=conn.cursor()
		if info == 'getall':
			x = c.execute("select * from Datalog where status LIKE ?", ('unsolved',)).fetchall()
			return json.dumps(x)
		elif info == 'getid':
			x = c.execute("select * from Datalog where Id=:x and status=:y",{"x":id,"y":status}).fetchall()
			return json.dumps(x)
		elif info == 'getlocal':
			x = c.execute("select * from Datalog where city=:x and country=:y and status=:z",{"x":city,"y":country,"z":status}).fetchall()
			return json.dumps(x)
		elif info == 'getalert':
			x = c.execute("select * from Datalog where alerts LIKE ?", (alerts,)).fetchall()
			return json.dumps(x)
		elif info == 'delete' :
			x = c.execute("update Datalog set status='solved' where AlertNr=?",(delete_pos,))
		#return alerts unsolved
		#http://localhost:8080/?&info=site	

		elif info=='ultrapassagem':
			if(status=='nao'):
				#não é possivel ultrapassar
				globalultrapassar.ultrapassar='nao'
			if(status=='sim'):
				globalultrapassar.ultrapassar='sim'
			return globalultrapassar.ultrapassar

		elif info == 'site':
			x = c.execute("select * from Datalog where status LIKE ?", ('unsolved',)).fetchall()
			a=json.dumps(x)
			f=open("texto.txt","w")
			f.write(a)
			f.close
			return a	
		else:
			x = c.execute("select * from Datalog")
			
		conn.commit()


	def POST(self,id,alerts,street,city,district,country,precision,latitude,longitude,ddatetime,status):
		conn = sqlite3.connect('database_v4_en.db')
		c = conn.cursor()
		x = c.execute("select * from Datalog where id=:x and alerts=:y and status=:z",{"x": id,"y":alerts,"z":status}).fetchall()
		
		if json.dumps(x) == '[]':
			ddatetime_start = ddatetime
			ddatetime_end = '---'
			status = 'unsolved' 
			c.execute("insert into Datalog (Id,alerts,street,city,district,country,precision,latitude,longitude,ddatetime_start,ddatetime_end,status) Values(?,?,?,?,?,?,?,?,?,?,?,?)",(id,alerts,street,city,district,country,precision,latitude,longitude,ddatetime_start,ddatetime_end,status))
		else:
			ddatetime_end = ddatetime			
			string = json.dumps(x)
			s = string.split(', ')	
			s2 = s[0].split('[')
			delete_pos = s2[len(s2)-1]
			x = c.execute("update Datalog set ddatetime_end=:x where id=:y and alerts=:z",{"x":ddatetime_end,"y":id,"z":alerts})
			x = c.execute("update Datalog set status='solved' where AlertNr=?",(delete_pos,))
		conn.commit()


if __name__ == '__main__':
    conf = { 
    'global' : {
        'server.socket_host' : 'localhost',
        'server.socket_port' : 8080,
        'server.thread_pool' : 8       #Configurations
        },
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }

 
    cherrypy.quickstart(StringGeneratorWebService(), '/', conf)