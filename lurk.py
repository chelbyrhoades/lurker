import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib
from bs4 import BeautifulSoup
import lxml.html
import random
import numpy as np
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import openpyxl
#other common libraries
from datetime import date
import time
import operator
import sys #getting input
import PySimpleGUI as sg

''' FUNCTIONS '''

def loadLinks(url):
	session = requests.Session()
	retry = Retry(connect=3, backoff_factor=0.5) # helps for politeness
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)

	html = requests.get(url).content
	bsO = BeautifulSoup(html, 'lxml')
	links = bsO.findAll('a')
	finalLinks = set()
	for link in links:               #got this from Beautiful Soup documentation.
		finalLinks.add(link.attrs['href'])
	return finalLinks

#checking to see if the url is broken. We don't like broken urls.
def checkUrl(url):
	p = urlparse(url)
	conn = httplib.HTTPConnection(p.netloc)
	conn.request('HEAD', p.path)
	resp = conn.getresponse()
	return resp.status < 400


#opening and starting the outfile
outFile = open('report.txt', 'w')
today = date.today()
outFile.write('LURKER REPORT\nGENERATED ON: {}'.format(today))


def visualGUI(notInIt):
	sg.theme('Dark Blue 3')	# Add a touch of color
	jokeList = ['What do you call a hill full of cats?\n A meow-ntain', 'Two guys walk into a bar. The third one ducks.', 'How many programmers does it take to change a lightbulb? None. Its a hardware problem.']

# All the stuff inside your window.
	layout = [
			[sg.Text('Welcome to Lurker! Ready to search?'), sg.Text('      ', key='-OUTPUT-')],
			[sg.Text()],
			[sg.Button('Search'), sg.Button('Joke'), sg.Button('More info'),sg.Button('Stop')]
			]
# Create the Window
	info = "Disallowed path found using the robots.txt file: " + notInIt
	info2 = 'I stored the tfidf in a dataframe, then transformed it using cosine similarity.'
	info3 = "I changed quite a bit with these files - previously, my Lurker had been reading files that it shouldn't have, as well as it didn't have a cool GUI."
	info4 = "This Lurker stores html, php, and text files and uses the data for the search"
	info5 = "I used sklearn's tfidfVectorizer and CosineSimilarity libraries in order to be able to search multiple terms"
	window = sg.Window('Lurker Mainframe', layout, location=(800,600))
	win2_active = False
	i=0
	while True:             # Event Loop
		event, values = window.read(timeout=100)
		if event != sg.TIMEOUT_KEY:
			print(i, event, values)
		if event in(None, 'More info'):
			sg.popup(info, info2, info3, info4, info5)
		if event in (None, 'Stop'):
			break
		elif event == 'Joke':
			sg.popup(random.choice(jokeList))
		i+=1
		if event == 'Search' and not win2_active:     # only run if not already showing a window2
			win2_active = True
	        # window 2 layout - note - must be "new" every time a window is created
			layout2 = [
				[sg.Text('Enter a search query:')],
				[sg.Input(key='-IN-')],
				[sg.Button('Show'), sg.Button('Stop')]
					]
			window2 = sg.Window('Lurker Search', layout2)
	    # Read window 2's events.  Must use timeout of 0
		cat = ['dog', 'bill'] #change this
		if win2_active:
	        # print("reading 2")
			event, values = window2.read(timeout=100)
	        # print("win2 ", event)
			if event != sg.TIMEOUT_KEY:
				print("win2 ", event)
			if event == 'Stop' or event is None:
	            # print("Closing window 2", event)
				win2_active = False
				window2.close()
			if event == 'Show':
				sg.popup('You entered ', values['-IN-'])
				#send values['-IN-'] to the database to see if its in it
				#use the passed in to query
				#score, docurl, doctitle
				if values['-IN-'] not in cat:#change cat to the numpy tuple
					sg.popup('Sorry it isnt in database.')
			if values['-IN-'].lower() == 'stop':
				win2_active = False
				window2.close()
	window.close()


'''STARTING TO CRAWL'''
def dissing():
	disallowURL = []
#let's first find the disallowed files.
	result = os.popen("curl https://s2.smu.edu/~fmoore/robots.txt").read() #the robots.txt extension is where the disallowed files are.
	result_data_set = {"Disallowed":[], "Allowed":[]}

	for line in result.split("\n"):
		if line.startswith('Allow'):    # this is for allowed url
			result_data_set["Allowed"].append(line.split(': ')[1].split(' ')[0])    # to neglect the comments or other junk info
		elif line.startswith('Disallow'):    # this is for disallowed url
			result_data_set["Disallowed"].append(line.split(': ')[1].split(' ')[0])   # to neglect the comments or other junk info
			disallowURL.append(line.split(': ')[1].split(' ')[0])
	return disallowURL[0]





'''MAIN OF THE FUNCTION'''
if __name__=='__main__':
	notAllowed = dissing()
	visualGUI(notAllowed)
	#do the visual LAST so we don't recrawl the same data

