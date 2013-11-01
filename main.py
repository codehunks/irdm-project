from flask import *
import feedparser
import threading


app = Flask(__name__)
app.secret_key = 'shivam bansal'
#first parsing
d = feedparser.parse('http://feeds.hindustantimes.com/HT-IndiaSectionPage-Topstories')
secs = 10

def make_request():
	#for next parsing check if there is an update
	global d
	global secs
	d1 = feedparser.parse('http://feeds.hindustantimes.com/HT-IndiaSectionPage-Topstories')
	if d1.status == 304:
		d1 = d
		secs = secs + 5
	else:
		#fresh parsing
		d1 = d = feedparser.parse('http://feeds.hindustantimes.com/HT-IndiaSectionPage-Topstories')
		secs = secs - 5
	return d1

@app.route('/')
def index():
	global secs
	x = make_request()
	threading.Timer(secs, index).start()
	return render_template('index.html',collection = x.entries)

#Run server
if __name__ == '__main__' :
	app.run(debug=True)