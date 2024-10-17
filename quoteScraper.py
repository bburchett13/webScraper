from urllib.request import urlopen
import re

url = "http://olympus.realpython.org/profiles/dionysus"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)

namePattern = "<h2>.*?</h2>"

name_results = re.search(namePattern, html, re.IGNORECASE)

name = name_results.group()
name = re.sub("<.*?>", "", name)
name = re.sub(".*? ", "", name)

print(name)

colorPattern = "<br.*?>\n.*?\n</center.*?>"

color_results = re.search(colorPattern, html, re.IGNORECASE)

color = color_results.group()
color = re.sub("<.*?>", "", color)
color = re.sub(".*? ", "", color)


print(color)

# pattern = "<title.*?>.*?</title.*?>"

# match_results = re.search(pattern, html, re.IGNORECASE)

# title = match_results.group()
# title = re.sub("<.*?>", "", title)
# print(title)