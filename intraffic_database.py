import sqlite3
#create database
conn = sqlite3.connect('intraffic_database.db')

c=conn.cursor()
c.execute('''CREATE TABLE Datalog (AlertNr INTEGER PRIMARY KEY AUTOINCREMENT, Id text , alerts text, street text,city text,district text, country text, precision text, latitude text, longitude text, ddatetime_start text,ddatetime_end text, status text)''')
conn.commit()