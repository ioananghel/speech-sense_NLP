# Training for fake news detection

import numpy
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import warnings

dataFrame = pd.read_csv("data_sets/fake_news_train.csv")

dataFrame.fillna('', inplace=True)
dataFrame['label'] = dataFrame['label'].astype(int)

# TO DO: tokenize text -- find how and to what parts this method should be applied.
# word_tokenize()

x_dataFrame = dataFrame['title'] + dataFrame['text']
y_dataFrame = dataFrame['label']

x_dataFrame.dropna()

# VECTORIZATION
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

count_vectorizer = CountVectorizer()
count_vectorizer.fit_transform(x_dataFrame)

freq_term_matrix = count_vectorizer.transform(x_dataFrame)

tfidf = TfidfTransformer(norm = "l2")
tfidf.fit(freq_term_matrix)
tf_idf_matrix = tfidf.fit_transform(freq_term_matrix)

# print(tf_idf_matrix)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(tf_idf_matrix,y_dataFrame, random_state=0)

from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()
print(logreg.fit(x_train, y_train))
Accuracy = logreg.score(x_test, y_test)

print(Accuracy*100)

# import tensorflow as tf

# logreg.save('fake_news.h5')

# loaded_logreg = tf.keras.models.load_model('fake_news.h5')

import pickle

with open('fake_news.pkl', 'wb') as f:
    pickle.dump(logreg, f)

with open('fake_news_count_vectorizer.pickle', 'wb') as f:
    pickle.dump(count_vectorizer, f)

with open('tfidf_transformer.pickle', 'wb') as f:
    pickle.dump(tfidf, f)
