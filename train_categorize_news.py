import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.linear_model import LogisticRegression

dataFrame = pd.read_csv('data_sets/categorization_BBC.csv')

print("Categories: ", dataFrame['Category'].unique())

dataFrame['CategoryId'] = dataFrame['Category'].factorize()[0]

categories = dataFrame[['Category', 'CategoryId']].drop_duplicates().sort_values('CategoryId')

def remove_tags(text):
    remove = re.compile(r'')
  
    return re.sub(remove, '', text)

dataFrame['Text'] = dataFrame['Text'].apply(remove_tags)

def special_char(text):
    review = ''
    for ch in text:
        if ch.isalnum():
            review = review + ch
        else:
            review = review + ' '
    
    return review

dataFrame['Text'] = dataFrame['Text'].apply(special_char)

def convert_lower(text):
   return text.lower()

dataFrame['Text'] = dataFrame['Text'].apply(convert_lower)

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)

    return [ch for ch in words if ch not in stop_words]

dataFrame['Text'] = dataFrame['Text'].apply(remove_stopwords)

def lemmatize_word(text):
    wordnet = WordNetLemmatizer()

    return " ".join([wordnet.lemmatize(ch) for ch in text])

dataFrame['Text'] = dataFrame['Text'].apply(lemmatize_word)

x_dataFrame = dataFrame['Text']
y_dataFrame = dataFrame['CategoryId']

x = np.array(dataFrame.iloc[:,0].values)
y = np.array(dataFrame.CategoryId.values)
count_vectorizer = CountVectorizer(max_features = 5000)
x = count_vectorizer.fit_transform(dataFrame.Text).toarray()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 0, shuffle = True)

logreg = LogisticRegression()
print(logreg.fit(x_train, y_train))
Accuracy = logreg.score(x_test, y_test)

print(Accuracy*100)

import pickle

with open('categorize_news.pkl', 'wb') as f:
    pickle.dump(logreg, f)

with open('categorize_news_count_vectorizer.pickle', 'wb') as f:
    pickle.dump(count_vectorizer, f)
