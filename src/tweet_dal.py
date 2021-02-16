import tweepy
from tweepy import Stream

from tweepy.streaming import StreamListener

import csv
#Add your credentials here
twitter_keys = {
        'consumer_key':        '****',
        'consumer_secret':     '****',
        'access_token_key':    '****',
        'access_token_secret': '****'
    }

#Setup access to API
auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])
#KeyWords to pass for Stream API
keywords =  ['Canada', 'University', 'Dalhousie University', 'Halifax', 'Canada Education']
#Search query to pass for Search API
query="Canada OR University OR Dalhousie University OR Halifax OR Canada Education"



api = tweepy.API(auth)

#1750 tweets are collected using Stream API
class StdOutListener(StreamListener):
    def __init__(self):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0

    def on_status(self, status):
        self.num_tweets+=1
        if(self.num_tweets<=1750):
            with open('OutputStreaming.csv', 'a') as f:
                writer = csv.writer(f)
                if(status.user.location is not None):
                    loc=status.user.location
                else:
                    loc='NaN'
                if(status.place is not None):
                    place=status.place.name
                else:
                    place='Nan'
                
                    
                writer.writerow([status.author.screen_name, status.created_at, status.text,loc,place,status.retweeted,status.retweet_count])
            return True
        else:
            return False

    def on_error(self, status):
        print (status)
    
#Append tweets to csv file
with open('OutputStreaming.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Date', 'Text','Location','TweetedFromLocation','RetweetStatus','RetweetCount'])


#Stream API
twitterStream = Stream(auth,StdOutListener() )
twitterStream.filter(track=keywords, languages=["en"])


#1750 tweets are collected using Search API
#Search API
for tweet in tweepy.Cursor(api.search,q=query,
                           lang="en",
                           ).items(1750):
    with open('OutputStreaming.csv', 'a') as f:
                writer = csv.writer(f)
                if(tweet.user.location is not None):
                    loc=tweet.user.location
                else:
                    loc='NaN'
                if(tweet.place is not None):
                    place=tweet.place.name
                else:
                    place='Nan'
                
                    
                writer.writerow([tweet.author.screen_name, tweet.created_at, tweet.text,loc,place,tweet.retweeted,tweet.retweet_count])
    
f.close()
