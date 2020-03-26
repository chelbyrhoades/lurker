'''************************
Chelby Rhoades
************************'''
'''********IMPORTS***********'''
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import date
import time
import operator
from sklearn.feature_extraction.text import TfidfVectorizer #testing purposes only - I'm only using this to see the accuracy of my results.
from bs4 import BeautifulSoup #THIS IS ONE OF THE MOST USED ONES

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


'''*******FUNCTIONS********'''
#find all links on the page
def links(url):
    html = requests.get(url).content
    bsObj = BeautifulSoup(html, 'lxml')

    links = bsObj.findAll('a')
    finalLinks = set()
    for link in links:
        finalLinks.add(link.attrs['href'])
    print("**** IN LINKS ****")
    print(finalLinks)
    return finalLinks

def processLink(leUrl):
	words = []
	wordfreq = []
	robotWord = "robot"
	ommited = ['-','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 
'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

	robotFile = False
	time.sleep(5) #pause for a bit. We want to be polite.
	
	print("INSIDE PROCESSLINK : requesting: {}".format(leUrl))
	print(leUrl)

	url = session.get(leUrl)
	#url = requests.get(leUrl)#"http://s2.smu.edu/~fmoore") #should find schedule.htm
	pagetext = url.text
	soup = BeautifulSoup(pagetext, "html.parser")
	txt = soup.get_text()
	tokens = txt.split()
	totalWords = len(tokens)



	for w in tokens:
		if w == robotWord:
			robotFile = True
			break
		if w not in ommited:
			words.append(w)
			wordfreq.append(tokens.count(w)) #this is counting how many times the words appear in the document
	
	urlWithWordCount = (dict(sip(words, totalWords)))

	if robotFile == False:
		pairs = (dict(zip(words, wordfreq))) # putting the two lists together
		return pairs, words, urlWithWordCount
		# need a way to make sure it doesn't look in robot file
	#urlWithWordCount = (dict(zip(firstTokens, )))

#computing the TF
def computeTF(wordDict, bow):
	schoolName  = bow
	print(schoolName)

	tfDict = {}
	bowCount = len(bow)
	for word, count in wordDict.items():
		tfDict[word] = count/float(bowCount)
	print(tfDict)

def computeIDF(docList):
	idfDict = {}
	N = len(docsList)
	idfDict = dict.fromkeys(docList[0].keys(), 0)
	for doc in docList:
		for word, val in doc.items():
			if val > 0:
				idfDict[word] += 1
	for word, val in idfDict.items():
		idfDict[word] = math.log10(N / float(val))

	return idfDict

def computeTFIDF(tfBow, idfs):
	tfidf = {}
	for word, val in tfBow.items():
		tfidf[word] = val * idfs[word]
	return tdidf

'''******MAIN DRIVER*******'''
#variables
foundURLS = []
foundBanned = []
alreadySearchedURLS = []
unknownURLS = []
otherURLS = []
allWords = []

docsIndexed = 0
tf_idf = {}
#returnedWords is our main dictionary of words

#our first url - the given website
starterUrl = "https://s2.smu.edu/~fmoore"
bannedUrl = ["http://lyle.smu.edu",
"mailto:fmoore@lyle.smu.edu"]
alreadySearchedURLS.append(starterUrl)
returnedWords, firstTokens, lenDict = processLink(starterUrl)
allWords.append(firstTokens)
print(firstTokens)
newURLs = links(starterUrl)

#(dict(zip(words, wordfreq))
docsIndexed += 1

#get rid of possible urls that try to get out of the directory
for x in newURLs:
	if x in bannedUrl:
		foundBanned.append(x)
for y in foundBanned:
	newURLs.remove(y)

print("length of newURLS : {}".format(len(newURLs)))
for n in newURLs:
	print(n)
	# (.txt, .htm, .html, .php). 
	if n[-3:] == "htm" or n[-3:] == "txt" or n[-4:] == "html" or n[-3:] == "php":
		#https://s2.smu.edu/~fmoore/
		putTogether = "https://s2.smu.edu/~fmoore/" + n
		print("added : {}".format(putTogether))
		foundURLS.append(putTogether)

	else:
		print("not found: {}".format(n))
		unknownURLS.append(n)
'''
while len(foundURLS) > 0:
	for i in foundURLS:
		print("processing: {}".format(i))
		if i in alreadySearchedURLS:
			foundURLS.remove(i)
		else:
			time.sleep(2)
			newWords = processLink(i) #its a pair returned
			docsIndexed += 1
			#NEED TO MAKE SURE ITS NOT ROBOT FILE
			#if newWords['NULL'] != 'NULL': #make sure not to add robotFile
			returnedWords.update(newWords)
			newURLs2 = links(i)
			for a in newURLs2:
				if a not in alreadySearchedURLS:
					print("added")
					foundURLS.append(a)

		#remove it so we don't have an infinite loop
		alreadySearchedURLS.append(i)
		foundURLS.remove(i)

print("THE UNKNOWNS")
print(unknownURLS)
'''
#sortedPairs = dict(sorted(pairs.items(), key=operator.itemgetter(1),reverse=True))
#print('Dictionary in descending order by value : ',sortedPairs)

'''*********TFIDF**********'''

#tf is (count of word in the document) / (count of all words in the document)
leTF = computeTF(returnedWords, **lenDict) #pass the dictionary and the bag of words(our tokens)
print(leTF)
'''*********REPORT**********'''
outFile = open('report.txt', 'w')
today = date.today()
outFile.write('LURKER REPORT\nGENERATED ON: {}'.format(today))
outFile.write('\nDefinition of "word":')
outFile.write('\nNumber of documents indexed: {}'.format(docsIndexed))
outFile.write('\nNumber of words indexed: {}'.format(len(returnedWords)))
outFile.write('\nTerm-document frequency matrix:\n')
outFile.write("PUT HERE <>")
outFile.write('\nThe top 20 most commonly used words: ')
outFile.close()
'''

d)	Generate the term-document frequency matrix.  [25 points]
TBD

Within the website given, it is determined that the 20 most commonly used words and their frequencies are:
'''

'''*********TESTS**********'''
#I'm only using the sklearn tfidf vectorizing library to see if mine is correct
'''tfidf = TfidfVectorizer()
response = tfidf.fit_transform(words)
feature_names = tfidf.get_feature_names()
for col in response.nonzero()[1]:
    print (feature_names[col], ' - ', response[0, col])'''

