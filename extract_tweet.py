import tweepy 
import csv
import pandas as pd
# Fill the X's with the credentials obtained by 
# following the above mentioned procedure. 
consumer_key = "Lhqm7LAyIPQdKgPrDj3iQZ5sg"
consumer_secret = "1Kt40qZr55On3o9DIIJqR8RzXxQS9gF939pSYihjswbUfTPTf1"
access_key = "1176358507202801664-zaUv4OQT0SMpkqcD4PA7zySG1Cjene"
access_secret = "YIRA4nRsUW3Kiqu4c3MDmX7313Gkk2fIql8QVNJd2tVGk"


searched_tweets = []
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret) 
api = tweepy.API(auth,wait_on_rate_limit=True) 

tweets=[]

for tweet in tweepy.Cursor(api.search,q="pepsi",count=100, lang="en", result_type="recent", include_entities=True).items():
    tweets.append(tweet)
    if(len(tweets)>=1000):
        break

print(len(tweets))
tweets_df = pd.DataFrame(vars(tweets[i]) for i in range(len(tweets)))
tweets_df.to_csv("tweets.csv")