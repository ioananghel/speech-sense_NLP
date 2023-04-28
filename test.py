import pandas as pd
import pickle

# Load the saved model
with open('fake_news.pkl', 'rb') as file:
    loaded_logreg = pickle.load(file)

import pickle

with open('count_vectorizer.pickle', 'rb') as file:
    loaded_count_vectorizer = pickle.load(file)

with open('tfidf_transformer.pickle', 'rb') as file:
    loaded_tfidf_transformer = pickle.load(file)

test_df = pd.read_csv("data_sets/fake_news_test.csv")
# test_df = pd.read_csv("data_sets/test.csv")

test_df.fillna('', inplace=True)
# test_df['label'] = test_df['label'].astype(int)

test_df['content'] = test_df['title'] + ' ' + test_df['text']

# Vectorize the text data
x_test = loaded_count_vectorizer.transform(test_df['content'])
x_test_tfidf = loaded_tfidf_transformer.transform(x_test)

# Make predictions
predictions = loaded_logreg.predict(x_test_tfidf)

print(predictions)
# print(test_df['label'])

for i in range(0,2):
    if(predictions[i] == 0):
        print(test_df['content'][i])