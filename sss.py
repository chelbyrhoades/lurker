from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

f = open("doc1.txt")
doc1 = str.decode(f.read(), "UTF-8", "ignore")
f = open("doc2.txt")
doc2 = str.decode(f.read(), "UTF-8", "ignore")
f = open("doc3.txt")
doc3 = str.decode(f.read(), "UTF-8", "ignore")

train_set = ["spider",doc1, doc2, doc3]

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)  #finds the tfidf score with normalization
cosine = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix) #here the first element of tfidf_matrix_train is matched with other three elements

print(tfidf_matrix)
#cosine = cosine_similarity(tfidf_matrix[length-1], tfidf_matrix)
print(cosine)