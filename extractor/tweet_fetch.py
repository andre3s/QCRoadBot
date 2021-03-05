from extractor.utility import twitter_connection
import tweepy
import json

api = twitter_connection()

# Get tweet timeline from an specific user.
user_id = 'QcRoad'
number_of_tweets = 10
timeline = api.user_timeline(user_id=user_id, count=number_of_tweets, tweet_mode='extended')

# Get tweet mentions
statuses = api.mentions_timeline()
print(str(len(statuses)) + " number of statuses have been mentioned.")

tweets = tweepy.Cursor(api.mentions_timeline).items(number_of_tweets)
tweets_list = [[tweet.text, tweet.created_at, tweet.id_str, tweet.user.screen_name, tweet.coordinates, tweet.place,
                tweet.retweet_count, tweet.favorite_count, tweet.lang, tweet.source, tweet.in_reply_to_status_id_str,
                tweet.in_reply_to_user_id_str, tweet.is_quote_status, tweet.location] for tweet in tweets]

test = tweets[0]

print(test)
test2 = json.loads(str(test))