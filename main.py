from flask import *
import feedparser
import threading

app = Flask(__name__)
app.secret_key = 'shivam bansal'

#first parsing
dht = feedparser.parse('http://feeds.hindustantimes.com/HT-IndiaSectionPage-Topstories')
dzn = feedparser.parse('http://zeenews.india.com/rss/india-national-news.xml')
die = feedparser.parse('http://syndication.indianexpress.com/rss/latest-news.xml')

secs = 120

def normal():
	new_content = ""
	jsfile = open("static/js/timer.js", "rt")
	for line in jsfile: 
	 	new_content = new_content + line.replace("location","//location")
	jsfile.close()
	f = open('static/js/timer.js','w')
	f.write(new_content) 
	f.close()


def make_request():
	global d
	global secs
	interval = secs/10
	x = feedparser.parse('http://feeds.hindustantimes.com/HT-IndiaSectionPage-Topstories', etag=dht.etag)
	y = feedparser.parse('http://zeenews.india.com/rss/india-national-news.xml', etag=dzn.etag)
	z = feedparser.parse('http://syndication.indianexpress.com/rss/latest-news.xml', etag=die.etag)

	if x.status == 304 or y.status == 304 or z.status == 304:
		#not changed, increase the interval
		d1 = x
		secs = secs + interval
	else:
		#changed, reload and decrease the interval
		secs = secs - interval
		new_content = ""
		jsfile = open("static/js/timer.js", "rt")
		for line in jsfile: 
		 	new_content = new_content + line.replace("//location","location")
		jsfile.close()
		f = open('static/js/timer.js','w')
		f.write(new_content) 
		f.close()
		threading.Timer(2, normal).start()

@app.route('/')
def index():
	global secs
	threading.Timer(secs, make_request).start()
	return render_template('index.html', collection = dht.entries, collection2 = die.entries, collection3 = dzn.entries)
	
#Run server
if __name__ == '__main__' :
	app.run(debug=True)