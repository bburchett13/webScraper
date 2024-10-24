from urllib.request import urlopen, Request
import random
import mechanicalsoup
from bs4 import BeautifulSoup
import urllib

# Create browser
browser= mechanicalsoup.StatefulBrowser()

# Find random page number
pageNum = random.randint(1,100)

# Create URL with random page number from which to grab quote
url = "https://www.goodreads.com/quotes?page=" + str(pageNum)

# Create URL request with Firefox as the agent (otherwise we get SSL issues)
req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla'
    }
)

# Open the URL
page = urllib.request.urlopen(req)

# Parse URL using Beatiful Soup
soup = BeautifulSoup(page.read().decode('utf-8'), "html.parser")

# Find divs containing Quote Text
quoteDivs = soup.find_all('div', class_='quoteText')

# Grab a random quote from all quotes including author and source (if included)
randomQuote = random.choice(quoteDivs)

# Print Quote
print(randomQuote.text)

