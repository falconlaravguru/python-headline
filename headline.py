import feedparser

from flask import Flask

app = Flask(__name__)

BBC_RSS = "http://feeds.bbci.co.uk/news/rss.xml"

@app.route('/')
def Index():
    feed = feedparser.parse(BBC_RSS)
    first_article = feed['entries'][0]

    return """
        <html>
            <body>
                <h1> BBC Headlines </h1>
                <b> {0} </b> </br>
                <b> {1} </b> </br>
                <p> {2} </p> </br>
            </body>
        </html>
    """.format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))
    return "Here's no news."

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
    

