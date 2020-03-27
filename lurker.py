'''************************
Chelby Rhoades
************************'''
'''********IMPORTS***********'''
import requests
import numpy as np
from collections import Counter 
import urllib
from bs4 import BeautifulSoup 
import pandas as pd
import openpyxl
from sklearn.feature_extraction.text import TfidfVectorizer
import lxml.html
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import date
import time
import operator
import sys #getting input

inputNum = int(input("Enter a number: "))

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


outFile = open('report.txt', 'w')
today = date.today()
outFile.write('LURKER REPORT\nGENERATED ON: {}'.format(today))

'''*******FUNCTIONS********'''

def links(url):
    html = requests.get(url).content
    bsObj = BeautifulSoup(html, 'lxml')

    links = bsObj.findAll('a')
    finalLinks = set()
    for link in links:
        finalLinks.add(link.attrs['href'])
    return finalLinks

def processLink(leUrl):
	words = []
	wordfreq = []
	ommited = ['-','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 
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
	#title = soup.title.string
	title = "currently an error"
	txt = soup.get_text()
	tokens = txt.split()

	for w in tokens:
		if w not in ommited:
			words.append(w)
			wordfreq.append(tokens.count(w)) #this is counting how many times the words appear in the document

	pairs = (dict(zip(words, wordfreq))) # putting the two lists together
	return pairs, words, title


def broken(url) :
	if requests.get(url).status_code == 200:
		return False
	else:
		return True


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
togetherString = putTokensInOne(firstTokens)
df1 = pd.DataFrame({doctemp: [togetherString]})



if robotWord not in returnedWords:
	outFile.write("\nURL: {} TITLE: {}".format(starterUrl, leTitle))
	for tok in firstTokens:
		allWords.append(tok)
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
			#if n in processedURLs:
				#processedURLs.remove(n)
		elif n[-5:] == "here/":#/dontgohere/
			robotFile = True
		else:
			processedURLs.append(n)
#this doesn't make sense but it works
for i in processedURLs:
	x = i

count = 1
while docsIndexed < inputNum:
		print(x + " is our current person")
		if x in bannedUrl:
			break
		else:
			x = starterUrl + "/" + x
			alreadySearchedURLS.append(x)
			returnedWords, firstTokens, leTitle = processLink(x)
			outFile.write("\nURL: {} TITLE: {}".format(x, leTitle))
			for tok in firstTokens:
				allWords.append(tok)
			docsIndexed += 1
			togetherString = ""
			togetherString = putTokensInOne(firstTokens)
		#df1.insert(docsIndexed, {doctemp: [togetherString]})
		#df1 = pd.DataFrame.insert(0, })#{doctemp: [togetherString]})
		#df1.insert(0, 'Name', 'abc')
			name = 'doc' + str(count)
			df1.insert(0, name, togetherString)
			count += 1
		#df1[doctemp] = doctemp
			newURLs2 = links(x)
			print(newURLs2)
			for x in newURLs2:
				if x in bannedUrl:
					foundBanned.append(x)
					#processedURLs.remove(x)
				elif x[-3:] == "pdf":
					unknownURLS.append(n)
				elif x[-5:] == "here/":#/dontgohere/
					robotFile = True
				else:
					processedURLs.append(x)
			if len(processedURLs) > 1:
				x = processedURLs[count]



#use the processed URLs now
#for l in 
'''
for n in newURLs:
	status = broken(n)#check to see if its a broken link
	if status == True:
		blink.append(n)
	else:
	# (.txt, .htm, .html, .php). 
		if n[-3:] == "htm" or n[-3:] == "txt" or n[-4:] == "html" or n[-3:] == "php":
		#https://s2.smu.edu/~fmoore/
			if n[-8:] == "cow1.txt" or n[-8:] == "cow2.txt" or n[-8:] == "cow3.txt" or n[-8:] == "cow4.txt":
				putTogether = "https://s2.smu.edu/~fmoore/textfiles/" + n
			else:
				putTogether = "https://s2.smu.edu/~fmoore/" + n
			print(putTogether + " LOOKING ")
			print("added : {}".format(putTogether))
			foundURLS.append(putTogether)

		else:
			unknownURLS.append(n)
if inputNum	> len(foundURLS):
	print("I didn't find enough urls for that:(")
	rangeOfURLS = foundURLS
if inputNum =< len(foundURLS):
	rangeOfURLS = foundURLS[:inputNum]

for i in rangeOfURLS: #already searched initial one

	print("processing: {}".format(i))
	if i in alreadySearchedURLS:
		dupes.append(i) #duplicate document
	else:
		time.sleep(2)
		newWords, secondTokens, leTitle2 = processLink(i)
		outFile.write("URL: {} TITLE: {}".format(i, leTitle2))
		docsIndexed += 1
			#NEED TO MAKE SURE ITS NOT ROBOT FILE
			#if newWords['NULL'] != 'NULL': #make sure not to add robotFile
		returnedWords.update(newWords)
		newURLs2 = links(i)
		for a in newURLs2:
			if a not in alreadySearchedURLS:
				print("added")
				foundURLS.append(a)
			else:
				dupes.append(a)

	alreadySearchedURLS.append(i)
'''
#print('Dictionary in descending order by value : ',sortedPairs)

vectorizer = TfidfVectorizer()
doc_vec = vectorizer.fit_transform(df1.iloc[0])
df2 = pd.DataFrame(doc_vec.toarray().transpose(), index=vectorizer.get_feature_names())
df2.columns = df1.columns
print(df2)


'''*********TFIDF**********'''





'''*********REPORT**********'''
#sortedPairs = dict(sorted(allWords.items(), key=operator.itemgetter(1),reverse=True))
#top20Items = take(20, sortedPairs.iteritems())
#this is for the top 20 ^^^

#URL AND TITLES
outFile.write('\nDuplicate documents found: \n')
for i in dupes:
	outFile.write(str(i) + "\n")
#outFile.write(dupes)
outFile.write('\nBroken Links found: \n')
for b in blink:
	outFile.write(str(b) + "\n")
outFile.write('\nNon-texfiles Found: \n')
for u in unknownURLS:
	outFile.write(str(u) + "\n")
#outFile.write(unknownURLS)
outFile.write("\nDefinition of a 'word': In the realm of Web Crawling, a word is only as powerful as it's frequency. Meaning, if a word appears several times within a document, then it's ranking goes up. Uniqueness within words is also taken into account, such as a user looking for a specific website needs specific words to find it. A person could search for 'Sausage Biscuits' and find loads of results. It might not be the exact result that they're looking for. If they add 'Grand's Sausage Biscuits' to their search, the unique combination of words helps filter to what the user wants. The same is reflected in Web Crawling. Using tfidf as a mathematical filter, we can determine how much weight a word puts on a website.")
outFile.write('\n\nNumber of documents indexed: {}'.format(docsIndexed))
outFile.write('\n\nNumber of words indexed: {}'.format(len(allWords)))
outFile.write('\n\nTerm-document frequency matrix:\n')
outFile.write('The tfidf is printed to the terminal until further notice')
outFile.write('\n\nThe top 20 most commonly used words: \n')
#here's where collections comes into play
Counter = Counter(allWords)
most_occur = Counter.most_common(20)
for t in most_occur:
  outFile.write(' '.join(str(s) for s in t) + '\n')

outFile.close()

