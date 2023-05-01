import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import make_scorer, roc_curve, roc_auc_score
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB


dataFrame = pd.read_csv('data_sets/categorization_BBC.csv')

print("Categories: ", dataFrame['Category'].unique())

dataFrame['CategoryId'] = dataFrame['Category'].factorize()[0]

categories = dataFrame[['Category', 'CategoryId']].drop_duplicates().sort_values('CategoryId')

def remove_tags(text):
    remove = re.compile(r'')
  
    return re.sub(remove, '', text)

dataFrame['Text'] = dataFrame['Text'].apply(remove_tags)

def special_char(text):
    reviews = ''
    for x in text:
        if x.isalnum():
            reviews = reviews + x
        else:
            reviews = reviews + ' '
    
    return reviews

dataFrame['Text'] = dataFrame['Text'].apply(special_char)

def convert_lower(text):
   return text.lower()

dataFrame['Text'] = dataFrame['Text'].apply(convert_lower)

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)

    return [x for x in words if x not in stop_words]

dataFrame['Text'] = dataFrame['Text'].apply(remove_stopwords)

def lemmatize_word(text):
    wordnet = WordNetLemmatizer()

    return " ".join([wordnet.lemmatize(word) for word in text])

dataFrame['Text'] = dataFrame['Text'].apply(lemmatize_word)

x_dataFrame = dataFrame['Text']
y_dataFrame = dataFrame['CategoryId']

x = np.array(dataFrame.iloc[:,0].values)
y = np.array(dataFrame.CategoryId.values)
count_vectorizer = CountVectorizer(max_features = 5000)
x = count_vectorizer.fit_transform(dataFrame.Text).toarray()
# print("X.shape = ",x.shape)
# print("y.shape = ",y.shape)

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
