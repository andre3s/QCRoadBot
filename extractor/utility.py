from datetime import datetime
import tweepy
import logging

from extractor.settings import twitter_api_key, twitter_api_secret_key, twitter_access_token, \
    twitter_access_token_secret

logger = logging.getLogger()


def get_timestamp():
    tmp_datetime_obj = datetime.now()
    datetime_obj = tmp_datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    return datetime_obj


def twitter_connection():
    auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error('Error during authentication.', exc_info=True)
        raise e
    logger.info('API successfully created.')

    return api


def tweet_sender(message):
    api = twitter_connection()
    try:
        api.update_status(message)
    except tweepy.TweepError as e:
        logger.error('Not able to tweet the message.', exc_info=True)
        print(e.reason)

