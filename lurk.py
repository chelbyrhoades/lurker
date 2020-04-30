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
	sg.theme('Dark Blue 3')	# Add a touch of color
	lis = ['twelve', 'five']
# All the stuff inside your window.
	layout = [
			[sg.Text('This is the FIRST WINDOW'), sg.Text('      ', key='-OUTPUT-')],
			[sg.Text()],
			[sg.Button('Launch 2nd Window'), sg.Button('Popup'), sg.Button('Stop')]
			]
# Create the Window
	
	window = sg.Window('Window Title', layout, location=(800,600))
	win2_active = False
	i=0
	while True:             # Event Loop
		event, values = window.read(timeout=100)
		if event != sg.TIMEOUT_KEY:
			print(i, event, values)
		if event in (None, 'Stop'):
			break
		elif event == 'Popup':
			sg.popup('This is a BLOCKING popup','all windows remain inactive while popup active')
		i+=1
		if event == 'Launch 2nd Window' and not win2_active:     # only run if not already showing a window2
			win2_active = True
	        # window 2 layout - note - must be "new" every time a window is created
			layout2 = [
				[sg.Text('The second window')],
				[sg.Input(key='-IN-')],
				[sg.Button('Show'), sg.Button('Stop')]
					]
			window2 = sg.Window('Second Window', layout2)
	    # Read window 2's events.  Must use timeout of 0
		cat = ['dog', 'bill']
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
				if values['-IN-'] not in cat:
					sg.popup('Sorry it isnt in database.')
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



