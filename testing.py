from flask import *
import feedparser
import threading
import execjs

app = Flask(__name__)
app.secret_key = 'shivam bansal'

#first parsing
d = feedparser.parse('http://feeds.hindustantimes.com/HT-IndiaSectionPage-Topstories')
secs = 3
interval = 2

def make_request():
	ctx1 = execjs.compile(""" function loadnew(){ location.reload(true); }""")
	ctx1.call("loadnew")

@app.route('/')
def index():
	global secs
	threading.Timer(secs, make_request).start()
	return render_template('index.html',collection = d.entries)
	

#Run server
if __name__ == '__main__' :
	app.run(debug=True)