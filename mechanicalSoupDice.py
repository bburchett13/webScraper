import mechanicalsoup
import time

browser = mechanicalsoup.StatefulBrowser()

for i in range(4):
    url = "http://olympus.realpython.org/dice"

    webpage = browser.get(url)

    html = webpage.soup

    tag = webpage.soup.select("#result")[0]

    result = tag.text

    print(f"The result of your dice roll is: {result}")
    if i < 3:
        time.sleep(10)