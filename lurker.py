'''************************
Chelby Rhoades
TO RUN: Mac: python3 lurker.py
************************'''
'''********IMPORTS***********'''
#libraries used for searching the web/parsing urls
#common libraries
from datetime import date
import time
import operator
import sys #getting input
import os
import random
import requests
#for http searching
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib
from bs4 import BeautifulSoup
import lxml.html
import PySimpleGUI as sg
#from urlparse import urlparse
#scientific computing libraries
import numpy as np
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy.spatial.distance import cosine
import openpyxl

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

def visualGUI(notInIt, data, inputNum, bagOfWords):
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
	info6 = "The search is buggy right now. It should print out to queryOut.xlxs"
	window = sg.Window('Lurker Mainframe', layout, location=(800,600))
	win2_active = False
	i=0
	while True:             # Event Loop
		event, values = window.read(timeout=100)
		count = 0
		if event != sg.TIMEOUT_KEY:
			print(i, event, values)
		if event in(None, 'More info'):
			sg.popup(info, info2, info3, info4, info5, info6)
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

				#ind = pd.Index(data)
				#if ind.str.contains(values['-IN-'], regex=False) == False:
				#	
				if values['-IN-'] not in bagOfWords:
					sg.popup('Sorry it isnt in database.')
				#if(len(data[].str.contains('Mel'))>0):
    			#	print("Name Present")
					
				else:
					queryW = str(values['-IN-'])
					listOfCosines = querySearch(values['-IN-'], df1, inputNum, count)
					count += 1
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

'''*******FUNCTIONS********'''

#this looks for possible links given the url
def links(url):
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

#processing the url's contents
def processLink(leUrl):
	words = []
	wordfreq = []
 #I put common stop words in this
	ommited = ['[',']','(',')','}','{',' ', ';', '=', '/', ',','-','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
	robotFile = False
	time.sleep(5) #pause for a bit. We want to be polite.
	#print("INSIDE PROCESSLINK : requesting: {}".format(leUrl))

	url = session.get(leUrl)

	#url = requests.get(leUrl)#"http://s2.smu.edu/~fmoore") #should find schedule.htm
	pagetext = url.text
	soup = BeautifulSoup(pagetext, "html.parser")
	
	#page = urllib.request.urlopen(leUrl)
	#html = BeautifulSoup(page.read(), 'html.parser')
	#title = html.title.string
	title = 'placeholder'

	txt = soup.get_text()
	tokens = txt.split()
    
    
	for w in tokens:
		result = ''.join([i for i in w if not i.isdigit()])
		w = result
		#doing this twice for those words that start like 12Apr
		if w not in ommited:
			words.append(w)
			wordfreq.append(tokens.count(w)) #this is counting how many times the words appear in the document

	pairs = (dict(zip(words, wordfreq))) # putting the two lists together
	return pairs, words, title


def putTokensInOne(listTok):
	leString = ""
	for e in listTok:
		leString = leString + e + " "
	return leString


def getTitle(link):
	page = urllib.request.urlopen('http://en.wikipedia.org')
	html = BeautifulSoup(page.read(), 'html.parser')
	print(html.title.string)
	return html.title.string

def querySearch(queryTerm, data, numDocs, qWord):
	count = 0
	#vectorizer = TfidfVectorizer()
	qWord = 'query' + str(count)
	data.insert(0, 'query', queryTerm)
	
	
	dat = pd.DataFrame(data.iloc[0]) #puts the data into a frame
	print(dat)
	dat.to_excel('queryOut.xlsx') #
	tfidf = TfidfVectorizer().fit_transform(data)
	cosine_similarities = linear_kernel(tfidf[0:numDocs-1], tfidf).flatten()
	print(cosine_similarities)
	cosine_similarities.max(axis = 0)
	
	'''df2 = pd.DataFrame(doc_vec.toarray().transpose(), index=vectorizer.get_feature_names())
	df2.columns = data.columns
	for i in range(0, numDocs):
		sim = (1 - cosine(queryTerm, data.iloc[i]))
		similarities.update({data[i] : sim})

	print(similarities)'''

	#df2.to_excel("output.xlsx")
	return cosine_similarities



'''******MAIN DRIVER*******'''
#variables
notAllowed = dissing()
foundURLS = []
foundBanned = []
alreadySearchedURLS = []
unknownURLS = []
otherURLS = []
allWords = []
dupes = [] #duplicates
blink = [] #the broken ones
robotWord = "noindex"

docsIndexed = 0
tf_idf = {}
#returnedWords is our main dictionary of words

#our first url - the given website
starterUrl = "https://s2.smu.edu/~fmoore"
bannedUrl = ["http://lyle.smu.edu",
"mailto:fmoore@lyle.smu.edu", "https://s2.smu.edu/~fmoore/dontgohere", "https://s2.smu.edu/~fmoore/dontgohere/badfile2.html", "https://s2.smu.edu/~fmoore/misc/noindex.html", "https://www.smu.edu/EnrollmentServices/Registrar/Enrollment/FinalExamSchedule/Spring2020", "http://lyle.smu.edu"] #I've gotten these files and they aren't supposed to be found.
#the robots.txt file disallowed /dontgohere specifically
notAllowed = dissing()
#getting the title

alreadySearchedURLS.append(starterUrl)
returnedWords, firstTokens, leTitle = processLink(starterUrl)
doctemp = "doc" + str(docsIndexed)
for tok in firstTokens:
		allWords.append(tok)
togetherString = putTokensInOne(firstTokens)
df1 = pd.DataFrame({'placeholder': ['this is to start dataframe']})



if robotWord not in returnedWords:
	outFile.write("\nURL: {} TITLE: {}".format(starterUrl, leTitle))
	newURLs = links(starterUrl)
	docsIndexed += 1

processedURLs = []

#get rid of possible urls that try to get out of the directory
for a in newURLs:
	if a in bannedUrl:
		foundBanned.append(a)
for y in foundBanned:
	newURLs.remove(y)
for n in newURLs: #pdf png htm html txt php ~fmoore.
	if n[-3:] == "png":
		unknownURLS.append(n)
		foundBanned.append(n)
	if n not in bannedUrl:
		if n[-3:] == "pdf" or n[-3:] == "jpg":
			unknownURLS.append(n)
			foundBanned.append(n)
		elif n[:10] == "dontgohere":#/dontgohere/
			robotFile = True
		else:
			processedURLs.append(n)

for i in processedURLs:	#this doesn't make sense but it works. I'll look into it further
	x = i

count = 1
weDontLike = "/dontgohere"
while docsIndexed < inputNum:
		print(x)
		if x in bannedUrl or weDontLike in x or 'noindex' in x or 'does_not_exist' in x:
			print("found a file we don't wanna mess with (could be for various reasons): {}".format(x))
			break
		else:
			print('loading...')
			tempx = x
			x = starterUrl + "/" + x
			alreadySearchedURLS.append(x) 
			returnedWords, firstTokens, leTitle = processLink(x)
			outFile.write("\nURL: {} TITLE: {}".format(x, leTitle))
			for tok in firstTokens:
				allWords.append(tok)
			docsIndexed += 1
			togetherString = ""
			togetherString = putTokensInOne(firstTokens)
			df1.insert(0, tempx, togetherString)
			count += 1
			newURLs2 = links(x)
			for x in newURLs2:
				print('.\n')

				if x in bannedUrl or x == 'dontgohere/badfile1.html': #we don't want that file
					foundBanned.append(x)
					disallowed = x
				elif x[-3:] == "pdf" or x[-4:] == "xlsx" or x[-4:] == "pptx":
					unknownURLS.append(x)
				elif x[-5:] == "here/":#/dontgohere/
					robotFile = True
				else:
					processedURLs.append(x)
			if len(processedURLs) > 1:
				x = processedURLs[count]

def split_line(text):
	result = []
    # split the text
	words = text.split()
	for word in words:
		result.append(word)
	return result

'''*********TFIDF**********'''

print("\n\n**********\n")
countOut = 0
using = int(input("GUI on, yes or no? Enter 1 for yes, 2 for no"))
if using == 1:
	visualGUI(notAllowed, df1, inputNum, allWords)
else:
	trying = input('What would you like to search?')
	listOfWords = split_line(trying)

	for i in listOfWords:
		i = i.lower().strip()
		listOfCosines = querySearch(i, df1, inputNum, countOut)
		countOut += 1


#print(df3)


print("\n\n**********\n")



'''******FINALIZING REPORT*******'''

#URL AND TITLES
outFile.write('\nDuplicate documents found: \n')
for i in dupes:
	outFile.write(str(i) + "\n")

outFile.write('\nBroken Links found: \n')
for b in blink:
	outFile.write(str(b) + "\n")
outFile.write('\nNon-textfiles Found: \n')
for u in unknownURLS:
	outFile.write(str(u) + "\n")

outFile.write("\nDefinition of a 'word': \nIn the realm of Web Crawling, a word is only as powerful as it's frequency. Meaning, if a word appears several times within a document, then it's ranking goes up. Uniqueness within words is also taken into account, such as a user looking for a specific website needs specific words to find it. A person could search for 'Sausage Biscuits' and find loads of results. It might not be the exact result that they're looking for. If they add 'Grand's Sausage Biscuits' to their search, the unique combination of words helps filter to what the user wants. The same is reflected in Web Crawling. Using tfidf as a mathematical filter, we can determine how much weight a word puts on a website.")
outFile.write('\n\nNumber of documents indexed: {}'.format(docsIndexed))
outFile.write('\n\nNumber of words indexed: {}'.format(len(allWords)))
outFile.write('\n\nTerm-document frequency matrix:\n')
outFile.write('The tfidf is printed to the terminal as well as matrix.csv')
outFile.write('\n\nThe top 20 most commonly used words and the amount of times that they are used: \n')
#here's where collections comes into play
Counter = Counter(allWords)
most_occur = Counter.most_common(20)
for t in most_occur:
  outFile.write(' '.join(str(s) for s in t) + '\n')

#df2.to_csv(r'/Users/ChelbyRhoades/Desktop/lurker/matrix.csv', index = True)
outFile.write('\n The disallowed file was: {}'.format(disallowed))
outFile.close()

