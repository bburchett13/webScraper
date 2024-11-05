from urllib.request import urlopen, Request
import random
import mechanicalsoup
from bs4 import BeautifulSoup
import urllib
import webbrowser
from threading import Timer
import ssl
from flask import Flask, render_template

# Create browser
browser= mechanicalsoup.StatefulBrowser()

# Find random page number
pageNum = random.randint(1,100)

# Create URL with random page number from which to grab quote
url = "https://www.goodreads.com/quotes?page=" + str(pageNum)

# html = requests.get(url)

# soup = BeautifulSoup(html.text, "html.parser")

# metadata = soup.find_all('meta')

# Create URL request with Firefox as the agent (otherwise we get SSL issues)
context = ssl._create_unverified_context()
req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Chrome'
    }
)

# Open the URL
page = urllib.request.urlopen(req, context=context)
# print(metadata)
# # Parse URL using Beatiful Soup
soup = BeautifulSoup(page.read().decode('utf-8'), "html.parser")

# Find divs containing Quote Text
quoteDivs = soup.find_all('div', class_='quoteText')

# Grab a random quote from all quotes including author and source (if included)
# randomQuote = random.choice(quoteDivs)

# Print Quote
# print(randomQuote.text)

app = Flask(__name__)

@app.route("/")
def index():
    randomQuote = random.choice(quoteDivs)
    my_string = randomQuote.text

    return render_template('index.html', my_string=my_string)

def open_browser():
      webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    app.run(debug=True)
    # Timer(1, open_browser).start()
    # app.run(port=2000)