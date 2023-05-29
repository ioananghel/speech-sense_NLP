import pandas as pd
import pickle
from .models import Articles
from . import db

with open('fake_news.pkl', 'rb') as file:
    loaded_logreg = pickle.load(file)

with open('fake_news_count_vectorizer.pickle', 'rb') as file:
    loaded_count_vectorizer = pickle.load(file)

with open('tfidf_transformer.pickle', 'rb') as file:
    loaded_tfidf_transformer = pickle.load(file)

# test_df = pd.read_csv("data_sets/fake_news_test.csv")
test_df = pd.read_csv("data_sets/categorization_BBC.csv")


test_df.fillna('', inplace=True)
# test_df['label'] = test_df['label'].astype(int)

# test_df['content'] = test_df['title'] + ' ' + test_df['text']
test_df['content'] = test_df['Text']


# Vectorize the text data
x_test = loaded_count_vectorizer.transform(test_df['content'])
x_test_tfidf = loaded_tfidf_transformer.transform(x_test)

# Make predictions
predictions = loaded_logreg.predict(x_test_tfidf)

print(predictions)
# print(test_df['label'])

# for i in range(0,2):
#     if(predictions[i] == 0):
#         print(test_df['content'][i])

test_df['trust_prediction'] = predictions

fake_news = test_df[test_df['trust_prediction'] == 1]

trustworthy_news = test_df[test_df['trust_prediction'] == 0]

print(fake_news.head())
print(trustworthy_news.head())

with open('categorize_news.pkl', 'rb') as file:
    loaded_logreg = pickle.load(file)

with open('categorize_news_count_vectorizer.pickle', 'rb') as file:
    loaded_count_vectorizer = pickle.load(file)

# test_df = trustworthy_news

print(test_df.head())
# test_df['content'] = test_df['title'] + ' ' + test_df['text']
test_df['content'] = test_df['Text']

# Vectorize the text data
x_test = loaded_count_vectorizer.transform(test_df['content'])

# Make predictions
predictions = loaded_logreg.predict(x_test)

print(predictions)

test_df['category_predictions'] = predictions

business = test_df[test_df['category_predictions'] == 0]
tech = test_df[test_df['category_predictions'] == 1]
politics = test_df[test_df['category_predictions'] == 2]
sport = test_df[test_df['category_predictions'] == 3]
entertainment = test_df[test_df['category_predictions'] == 4]

print(business.head())
print(tech.head())
print(politics.head())
print(sport.head())
print(entertainment.head())

test_df["category_predictions"][test_df['category_predictions'] == 0] = "business"
test_df["category_predictions"][test_df['category_predictions'] == 1] = "tech"
test_df["category_predictions"][test_df['category_predictions'] == 2] = "politics"
test_df["category_predictions"][test_df['category_predictions'] == 3] = "sport"
test_df["category_predictions"][test_df['category_predictions'] == 4] = "entertainment"


# for i in range(0, len(test_df)):
#      article = test_df.iloc[i]
#      new_article = Articles(title=article["content"], content=article["content"], sentiment=article["trust_prediction"], category=article["category_predictions"])  #providing the schema for the article 
#      db.session.add(new_article) #adding the article to the database 
#      db.session.commit()
#      # flash('Article added!', category='success')
