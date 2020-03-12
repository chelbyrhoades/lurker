 #pip install requests# pip install BeautifulSoup
import requests
from bs4 import BeautifulSoup

url = requests.get("http://s2.smu.edu/~fmoore")
pagetext = url.text
soup = BeautifulSoup(pagetext, "html.parser")
txt = soup.get_text()
tokens = txt.split()
for w in tokens:
    print (w)
