import httpx
import json
from parsel import Selector
import csv

DEFAULT_HEADERS = {
    # lets use Chrome browser on Windows:
    "User-Agent": "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=-1.9,image/webp,image/apng,*/*;q=0.8",
}
# then we should create a persistent HTTP client:
client = httpx.Client(headers=DEFAULT_HEADERS)

response_first = client.get("https://books.toscrape.com")

selector = Selector(text=response_first.text)
print(response_first.url)
def parse_books(response: httpx.Response):
    selector = Selector(text=response.text)
    parsed = []
    for book in selector.css('.row .col-xs-6'):
        # note that web pages use relative urls (e.g. /jobs/1234)
        # which we can convert to absolute urls (e.g. remotepython.com/jobs/1234 )
        relative_url = book.css('h3 a::attr(href)').get()
        absolute_url = response.url.join(relative_url)
        # rest of the data can be parsed using CSS or XPath selectors:
        parsed.append({
            "url" : str(absolute_url),
            "title" : book.css('h3 a::attr(title)').get(),
            "price" : book.css('.price_color ::text').get()[1:],
            # "thumbnail URL": str(response.url.join(book.css('.image_container img::attr(src)').get())),
            # "availability": book.css('p.availability ::text').get()[1:],
        })
    return parsed

results = parse_books(response_first)

for i in range(2,50) :
    url_backHalf = "catalogue/page-{}.html".format(i)
    

    absolute_url = response_first.url.join(url_backHalf)
    response = client.get(absolute_url)
    results.extend(parse_books(response))


print(json.dumps(results, indent=2))
