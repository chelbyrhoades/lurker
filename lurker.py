'''************************
Chelby Rhoades
************************'''
'''********IMPORTS***********'''
import requests
import urllib
from bs4 import BeautifulSoup #THIS IS ONE OF THE MOST USED ONES
import lxml.html
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import date
import time
import operator



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
	title = soup.title.string
	txt = soup.get_text()
	tokens = txt.split()
	print(len(tokens))


	for w in tokens:
		if w == robotWord:
			robotFile = True
			break
		if w not in ommited:
			words.append(w)
			wordfreq.append(tokens.count(w)) #this is counting how many times the words appear in the document
	#counts = dict()

	#urlWithWordCount = (dict(zip(words, int(totalWords))))

	if robotFile == False:
		pairs = (dict(zip(words, wordfreq))) # putting the two lists together
		return pairs, words, title#, urlWithWordCount
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

#getting the title

alreadySearchedURLS.append(starterUrl)
returnedWords, firstTokens, leTitle = processLink(starterUrl)
outFile.write("\nURL: {} TITLE: {}".format(starterUrl, leTitle))
allWords.append(firstTokens)
print(firstTokens)
newURLs = links(starterUrl)
dupes = [] #duplicates

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
		unknownURLS.append(n)
'''
while len(foundURLS) > 0:
	for i in foundURLS:
		print("processing: {}".format(i))
		if i in alreadySearchedURLS:
			foundURLS.remove(i)
		else:
			time.sleep(2)
			newWords, secondTokens, leTitle2 = processLink(i) #its a pair returned
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

		#remove it so we don't have an infinite loop
		alreadySearchedURLS.append(i)
		foundURLS.remove(i)

print("THE UNKNOWNS")
print(unknownURLS)
'''

#print('Dictionary in descending order by value : ',sortedPairs)

'''*********TFIDF**********'''

#tf is (count of word in the document) / (count of all words in the document)
#leTF = computeTF(returnedWords, **lenDict) #pass the dictionary and the bag of words(our tokens)
#print(leTF)



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

outFile.write('\nNon-texfiles Found: \n')
for u in unknownURLS:
	outFile.write(str(u) + "\n")
#outFile.write(unknownURLS)
outFile.write("\nDefinition of a 'word': In the realm of Web Crawling, a word is only as powerful as it's frequency. Meaning, if a word appears several times within a document, then it's ranking goes up. Uniqueness within words is also taken into account, such as a user looking for a specific website needs specific words to find it. A person could search for 'Sausage Biscuits' and find loads of results. It might not be the exact result that they're looking for. If they add 'Grand's Sausage Biscuits' to their search, the unique combination of words helps filter to what the user wants. The same is reflected in Web Crawling. Using tfidf as a mathematical filter, we can determine how much weight a word puts on a website.")
outFile.write('\n\nNumber of documents indexed: {}'.format(docsIndexed))
outFile.write('\n\nNumber of words indexed: {}'.format(len(returnedWords)))
outFile.write('\n\nTerm-document frequency matrix:\n')
outFile.write("PUT HERE <>")
outFile.write('\n\nThe top 20 most commonly used words: \n')
#outFile.write(top20Items)
outFile.close()

