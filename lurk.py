import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib
from bs4 import BeautifulSoup
import lxml.html

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
def visualGUI():
	sg.theme('DarkAmber')	# Add a touch of color
	lis = ['twelve', 'five']
# All the stuff inside your window.
	layout = [[sg.Text('\n\n\n                                        Lurker: The Queen of Queries')],
				[sg.Text('\nPlease enter a search query: '), sg.InputText()],
				[sg.Button('Search'), sg.Button('Stop')] ]
	layout2 = [[sg.Text('\n\n\nYour query did not match anything in our database.')],
				[sg.Text('\nPlease try again'), sg.InputText()],
				[sg.Button('Continue'), sg.Button('Stop')] ]
# Create the Window
	window = sg.Window('Lurker', layout)
	window2 = sg.Window('Error!', layout2)
# Event Loop to process "events" and get the "values" of the inputs
	while True:
		event, values = window.read(timeout=100)
		if event in (None, 'Stop'):	# if user closes window or clicks cancel
			break
		if values[0].lower() == 'stop':
			break
		if values[0] not in lis and values[0].lower() != 'stop':
			#window = sg.Window('Error!', layout2)
			sg.popup('This is a block popup', 'all windows remain the same')

		print('You entered ', values[0])
	window.close()


'''STARTING TO CRAWL'''

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
print (disallowURL)







'''MAIN OF THE FUNCTION'''
if __name__=='__main__':
	words1 = ['Here comes the sun dun dun dun']
	words2 = ['Sweet dreams are made of these']
	words3 = ['There is a house in New Orleans']
	words4 = ['Dream on! Dream on!']
	words5 = ['Jenny, I got your number.']
	visualGUI()



