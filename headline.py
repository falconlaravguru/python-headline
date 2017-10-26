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

import datetime
from flask import make_response

app = Flask(__name__)

RSS_FEEDS = { 
    'bbc' : 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn' : 'http://rss.cnn.com/rss/edition.rss',
    'fox' : 'http://feeds.foxnews.com/foxnews/latest',
    'iol' : 'http://www.iol.co.za/cmlink/1.640',
}

DEFAULTS = {
    'publication':'bbc',
    'city':'Manchester,UK',
    'currency_from':'GBP',
    'currency_to':'USD'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=76cf4ebd7c79db726efc2ddeb6cd41b6"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=4e8eb525d0214a2f812745354e3f3f9d"

@app.route('/', methods=['GET','POST'])
def home():
    # get customized headlines, based on user input or default
    publication = get_fallback('publication') 
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = get_fallback('city')
    weather = get_weather(city)
    # get customized currency based on user input or default
    currency_from = get_fallback("currency_from")
    currency_to = get_fallback("currency_to")

    rate = get_rate(currency_from, currency_to)
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(render_template("home.html", articles=articles,
                                        weather=weather,
                                        currency_from=currency_from,
                                        currency_to=currency_to,
                                        rate=rate,
                                        currencies=sorted(currencies)))

    expiry_time = datetime.datetime.now() + datetime.timedelta(days=365)

    response.set_cookie("publication",publication,expires=expiry_time)
    response.set_cookie("city",city,expires=expiry_time)
    response.set_cookie("currency_from",currency_from,expires=expiry_time)
    response.set_cookie("currency_to",currency_to,expires=expiry_time)
    return response

def get_news(publication):
    if not publication or publication.lower() not in RSS_FEEDS :
        publication = DEFAULTS["publication"]
    else:
        publication = publication.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']

def get_weather(query):
    
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {
                    'description':parsed['weather'][0]['description'],
                    'temperature':parsed['main']['temp'],
                    'city':parsed['name']
                }
    return weather

def get_rate(frm,to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()

    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return ( to_rate/frm_rate, parsed.keys() )

def get_fallback(key):
    if request.form.get(key):
        return request.form.get(key)
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS['key']

if __name__ == '__main__':
    app.run(port = 5000, debug = True)


