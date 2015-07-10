import urllib2, time, traceback
from BeautifulSoup import BeautifulSoup
import sqlite3

books = { 
	'python':'http://www.yes24.com/24/goods/3432490',
	'lua':'http://www.yes24.com/24/goods/3081202',
	'cpp':'http://www.yes24.com/24/goods/2817935',
	'gamebot':'http://www.yes24.com/24/goods/2549646',
	'python2yol':'http://www.yes24.com/24/goods/1783933',
	'django':'http://www.yes24.com/24/goods/3348853'
}

def getContent( url ):
	req = urllib2.Request( url )
	response = urllib2.urlopen(req)
	return response.read()

class DB:
	"SQLITE3 wrapper class"
	def __init__(self):
		self.conn = sqlite3.connect('/var/www/book/mybookDB')
		self.cursor = self.conn.cursor()
		for title in books.keys():
			self.cursor.execute('CREATE TABLE IF NOT EXISTS %s(date text PRIMARY KEY, sale int)'%title)
			#self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS IDX001 ON %s(date)'%title)
		
	def __del__(self):
		self.conn.commit()
		self.cursor.close()

	def insertPython(self, title, date, sale):
		try:	
			self.cursor.execute("INSERT INTO %s VALUES ('%s',%d)"%(title,date,sale))
		except:
			print '%s : maybe already inserted'%title
			return 0
		else:
			print '%s: success'%title
			return 1

	def printPythonResultAll(self, title):
		self.cursor.execute('SELECT * FROM %s ORDER BY date ASC'%title)
		for row in self.cursor.fetchall():
			print row[1],

	def printPythonResult(self, title, num):
		self.cursor.execute('SELECT * FROM %s ORDER BY date DESC LIMIT %d'%(title,num))
		for row in self.cursor.fetchall():
			print row[0],'\t', row[1]

	def getResult(self, title, num=-1):
		if num==-1:
			self.cursor.execute('SELECT * FROM %s ORDER BY date DESC'%(title))
		else:
			self.cursor.execute('SELECT * FROM %s ORDER BY date DESC LIMIT %d'%(title,num))
		col1 = []
		col2 = []
		for row in self.cursor.fetchall():
			col1.append( row[0] )
			col2.append( row[1] )
		return col1, col2

if __name__ == "__main__":
	db=DB()
	curtime = time.localtime()
	curday = "%d/%02d/%02d"%(curtime[0],curtime[1],curtime[2])
	
	for title,url in books.items():
		content = getContent( url )
		soup = BeautifulSoup( content )
		
		a = soup('dt', {'class':'saleNum'})
		salenum = -1
		if len(a)>0:
			try:
				text = str( a[0].contents[0] ).split('|')[1]
				#print text
				splited = text.split(' ')
				for s in splited:
					if s.isdigit():
						salenum = int(s)
						break			
			except:
				traceback.print_exc()
				
			print title, ': try to insert :',curday, salenum
			db.insertPython( title, curday, salenum )
			
			print title, ': === recent 10 sale points ==='
			db.printPythonResult( title, 10 )
		
	time.sleep(5) # for reading results....
	
	
