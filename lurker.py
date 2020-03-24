#using beautiful soup and standard urllib
'''note - the urllib version used isn't compatible with earlier versions
	of urllib; so Python is required to be updated to version 3.
'''
import requests
import urllib.requests
import urllib.parser
from bs4 import BeautifulSoup


url = requests.get("http://s2.smu.edu/~fmoore")
pagetext = url.text
soup = BeautifulSoup(pagetext, "html.parser")
txt = soup.get_text()
tokens = txt.split()
for w in tokens:
    print (w)
