from extractor.utility import twitter_connection

api = twitter_connection()
res = api.home_timeline(count=2)

if res.status_code == 200:
    pass
else:
    message = 'Failed to retrieve tweets.'
    print(message)

