'''************************
Chelby Rhoades
************************'''
'''********IMPORTS***********'''
import requests
import time
import operator
#from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer #testing purposes only - I'm only using this to see the accuracy of my results.
from bs4 import BeautifulSoup #THIS IS ONE OF THE MOST USED ONES



'''*******FUNCTIONS********'''
#find all links on the page
def links(url):
    html = requests.get(url).content
    bsObj = BeautifulSoup(html, 'lxml')

    links = bsObj.findAll('a')
    finalLinks = set()
    for link in links:
        finalLinks.add(link.attrs['href'])
    return finalLinks


def computeTF(wordDict, bow):
	tfDict = {}
	bowCount = len(bow)
	for word, count in wordDict.items():
		tfDict[word] = count/float(bowCount)
	print(tfDict)

def processLink(urlList):
	robotWord = "robot"
	ommited = ['-','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 
'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

	robotFile = False
	time.sleep(5) #pause for a bit. We want to be polite.
	for i in urlList:
		url = requests.get(i)#"http://s2.smu.edu/~fmoore") #should find schedule.htm
		pagetext = url.text
		soup = BeautifulSoup(pagetext, "html.parser")
		txt = soup.get_text()
		tokens = txt.split()

	for w in tokens:
		if w == robotWord:
			robotFile = True
			break
		if w not in ommited:
			words.append(w)
			wordfreq.append(tokens.count(w)) #this is counting how many times the words appear in the document
	
	if robotFile == False:
		return pairs = (dict(zip(words, wordfreq))) # putting the two lists together
	else:
		return pairs = (dict(zip("NULL", "NULL")))



'''******MAIN DRIVER*******'''
#variables
words = []
wordfreq = []
foundURLS = []
alreadySearchedURLS = []
#STOP WORDS LIST INSIDE OF A LIST

#LET'S START!
#our first url - the given website
starterUrl = ["https://s2.smu.edu/~fmoore"]
alreadySearchedURLS.insert(starterUrl[0])

returnedWords = processLink(starterUrl)


#sortedPairs = dict(sorted(pairs.items(), key=operator.itemgetter(1),reverse=True))
#print('Dictionary in descending order by value : ',sortedPairs)



#tf is (count of word in the document) / (count of all words in the document)
computeTF(pairs, tokens) #pass the dictionary and the bag of words(our tokens)




'''*********TESTS**********'''
#I'm only using the sklearn tfidf vectorizing library to see if mine is correct
'''tfidf = TfidfVectorizer()
response = tfidf.fit_transform(words)
feature_names = tfidf.get_feature_names()
for col in response.nonzero()[1]:
    print (feature_names[col], ' - ', response[0, col])'''

