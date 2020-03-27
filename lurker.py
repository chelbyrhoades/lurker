'''************************
Chelby Rhoades
TO RUN: Mac: python3 lurker.py
************************'''
'''********IMPORTS***********'''
#libraries used for searching the web/parsing urls
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib
from bs4 import BeautifulSoup
import lxml.html
#from urlparse import urlparse
#scientific computing libraries
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
	title = "error for now"
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

'''******MAIN DRIVER*******'''
#variables
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

#getting the title

alreadySearchedURLS.append(starterUrl)
returnedWords, firstTokens, leTitle = processLink(starterUrl)
doctemp = "doc" + str(docsIndexed)
for tok in firstTokens:
		allWords.append(tok)
togetherString = putTokensInOne(firstTokens)
df1 = pd.DataFrame({'ROOT': [togetherString]})



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
for n in newURLs:
	if n not in bannedUrl:
		if n[-3:] == "pdf":
			unknownURLS.append(n)
		elif n[:10] == "dontgohere":#/dontgohere/
			robotFile = True
		else:
			processedURLs.append(n)

for i in processedURLs:	#this doesn't make sense but it works. I'll look into it further
	x = i

count = 1
while docsIndexed < inputNum:
		if x in bannedUrl:
			print("found a file we don't wanna mess with (could be for various reasons)")
			break
		else:
			print(x + " is our currently considered address")
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
				print('reviewing {}'.format(x))

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


'''*********TFIDF**********'''
vectorizer = TfidfVectorizer()
doc_vec = vectorizer.fit_transform(df1.iloc[0])
df2 = pd.DataFrame(doc_vec.toarray().transpose(), index=vectorizer.get_feature_names())
df2.columns = df1.columns
print(df2)


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

df2.to_csv(r'/Users/ChelbyRhoades/Desktop/lurker/matrix.csv', index = True)
outFile.write('\n The disallowed file was: {}'.format(disallowed))
outFile.close()

