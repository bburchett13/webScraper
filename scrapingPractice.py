import httpx
import json
from parsel import Selector

# first we need to configure default headers to avoid being blocked.
DEFAULT_HEADERS = {
    # lets use Chrome browser on Windows:
    "User-Agent": "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=-1.9,image/webp,image/apng,*/*;q=0.8",
}
# then we should create a persistent HTTP client:
client = httpx.Client(headers=DEFAULT_HEADERS)

# to start, let's scrape first page
response_first = client.get("https://www.remotepython.com/jobs/")

# and create a function to parse job listings from a page - we'll use this for all pages
def parse_jobs(response: httpx.Response):
    selector = Selector(text=response.text)
    parsed = []
    # find all job boxes and iterate through them:
    for job in selector.css('.box-list .item'):
        # note that web pages use relative urls (e.g. /jobs/1234)
        # which we can convert to absolute urls (e.g. remotepython.com/jobs/1234 )
        relative_url = job.css('h3 a::attr(href)').get()
        absolute_url = response.url.join(relative_url)
        # rest of the data can be parsed using CSS or XPath selectors:
        parsed.append({
            "url": str(absolute_url),
            "title": job.css('h3 a::text').get(),
            "company": job.css('h5 .color-black::text').get(),
            "location": job.css('h5 .color-white-mute::text').get(),
            "date": job.css('div>.color-white-mute::text').get('').split(': ')[-1],
            "short_description": job.xpath('.//h5/following-sibling::p[1]/text()').get("").strip(),
        })
    return parsed

results = parse_jobs(response_first)

# to scrape other pages we need to find their links and repeat the scrape process:
other_page_urls = Selector(text=response_first.text).css('.pagination a::attr(href)').getall()
for url in other_page_urls:
    # we need to turn relative urls (like ?page=2) to absolute urls (like http://remotepython.com/jobs?page=2)
    absolute_url = response_first.url.join(url)
    response = client.get(absolute_url)
    results.extend(parse_jobs(response))

#print as json 
print(json.dumps(results, indent=2))


