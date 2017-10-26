import feedparser

from flask import Flask

# Jinja template implemented
from flask import render_template
# Request context used
from flask import request
# Add weather data - OpenWeatherwithMap
import json
import urllib
import urllib2

app = Flask(__name__)

RSS_FEEDS = { 
    'bbc' : 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn' : 'http://rss.cnn.com/rss/edition.rss',
    'fox' : 'http://feeds.foxnews.com/foxnews/latest',
    'iol' : 'http://www.iol.co.za/cmlink/1.640',
}

@app.route('/', methods=['GET','POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS :
        publication = "bbc"
    else :
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    location = "London, UK"
    located_weather = get_weather(location)

    return render_template("home.html", 
                            articles = feed['entries'],
                            weather = located_weather)

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=76cf4ebd7c79db726efc2ddeb6cd41b6"
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed['weather'][0]['description'],
            "temperature": parsed['main']['temp'],
            "city": parsed['name']
        }
    return weather

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
    

