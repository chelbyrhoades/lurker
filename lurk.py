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
	return disallowURL

#this looks for possible links given the url
def links(url, disallowed):
	preferedTypes = ["htm", "php", "txt"]
	html = requests.get(url).content
	bsO = BeautifulSoup(html, 'lxml')
	links = bsO.findAll('a')
	finalLinks = set()
	resultLinks = []
	for link in links:               #got this from Beautiful Soup documentation.
		finalLinks.add(link.attrs['href'])

	for i in finalLinks:
		if i[-3:] in preferedTypes or i[-4] == "html" and disallowed not in i or i[-1] == '/':
			resultLinks.append(i)
	return resultLinks

def crawlFurther(path, beforePath, disallowed):
	lookat = beforePath + path

	print(lookat)
	leLinks = links(lookat, disallowed)
	for i in leLinks:
		i = path + '/' + i
	return leLinks



#starting a session and making sure we aren't being impolite
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

#opening and starting the outfile
outFile = open('report.txt', 'w')
today = date.today()
outFile.write('LURKER REPORT\nGENERATED ON: {}'.format(today))




if __name__=='__main__':
	allURLS = []
	alreadySearched = []
	disallowedURLS = dissing()
	webAddress = "https://s2.smu.edu/~fmoore/"
	allURLS.append(webAddress)
	print(disallowedURLS)
	gotInput = False

	print("Lurker: A Web Crawler\n")
	print('To properly see the readme, please consider reading it through the github website\n')
	print('The results will be in reports.txt and matrix.csv\n')
	print("************ Now let's begin! ************")
	#making sure a number is put in
	while gotInput != True:
		inputNum = int(input("\nEnter the number of files that you want to crawl: "))
		if inputNum > 0:
			gotInput = True

			flinks = links(webAddress, disallowedURLS)
			alreadySearched.append(webAddress)
			for lin in flinks:
				allURLS.append(lin)
#finding more links - digging deeper
			for i in flinks:
				moreLinks = crawlFurther(i, webAddress, disallowedURLS)
				alreadySearched.append(i)
			for lin in moreLinks:
				allURLS.append(lin)

		print(allURLS)
		for i in allURLS:
			if i not in alreadySearched:
				print("searching" + i)
				evenMoreLinks = crawlFurther(i, webAddress, disallowedURLS)
			else:
				print('already got it')
		print(evenMoreLinks)




