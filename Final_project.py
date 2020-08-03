import shutil
import tweepy
import requests
import os
import DB_Connection
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#sentiment Analysis
def vaderAnalysis(text):
    value = 0
    analyzer = SentimentIntensityAnalyzer()
    curr = analyzer.polarity_scores(text)
    if (curr['compound'] > -0.05 and curr['compound'] < 0.05):
        value = 0
    elif (curr['compound'] >= 0.05):
        value = 1
    elif (curr['compound'] <= -0.05):
        value = -1
    return value

#Private Keys
CONSUMER_KEY = "VSsukXgRg6LPo9PX8gkpx2HvI"
CONSUMER_SECRET = "cZzHo4gtL2h18pgzvzcUzPP4WuxFke7taI55GllDjjLCmeCY6k"
OAUTH_TOKEN = "818452111000240128-KFIFXKmEsc4s37lu5jRHK1wVh9jKtAW"
OAUTH_SECRET = "aR7TrRWKpXJrIOwkiDGDMWxlf9PccrEXPJyuWXpjf5qfY"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
api = tweepy.API(auth)

query = "#blackpeople"
print("###Tweet Fetching Mode")
tweets = [t for t in tweepy.Cursor(api.search,
                           q=query,
                           rpp=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items(500)]

print("####Tweets fetched")
link = []
i = 0
print("####Performing Sentiment Analysis on tweets")
print("####Insert tweets into database")
for tweet in tweets:
   for media in tweet.entities.get("media",[{}]):
      if not bool(media) == False:
          try:
              print(i)
              i = i + 1

              sentiment = vaderAnalysis(tweet.text)

              DB_Connection.insert(tweet.text,str(media['media_url_https']), sentiment)
              a =  link.append(media['media_url_https'])
          except:
              print("error occured")


print("####Save image to local disk")
for image_url in link:
    image_name = image_url.split('/')
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)
    # Open a local file with wb ( write binary ) permission.
    local_file = open(image_name[-1], 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp


