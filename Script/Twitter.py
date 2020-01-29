import os
import pandas as pd
import tweepy as tw
import json

#Set twitter api kei and parameter varius
def setAttr():
    consumer_key = 'pw0eWIQgm02PNGCEwt8dmEMSE'
    consumer_secret_key = 'IU18kd20PPhjZlanc3eE2S1DEgXARUr3DQpOFmAu11ErbNQcj1'
    access_token = '1126373990883319808-LdRh3RjseJK6mhduC16vHLtX65tWvB'
    access_token_secret = 'froKBiFQbDOtl0OrmFWIUu6N5PaWGJRAixFQON8dMnZjd'

    auth = tw.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    from_date = "2019-11-24"
    topic_channels = [
        # Photography
        {
            'topic': 'Photography',
            'account': '@NatGeoPhotos'
        },
        {
            'topic': 'Photography',
            'account': '@NASAHubble'
        },
        {
            'topic': 'Photography',
            'account': '@AP_Magazine'
        },
        # Science
        {
            'topic': 'Science',
            'account': '@NASA'
        },
        {
            'topic': 'Science',
            'account': '@sciencemagazine'
        },
        {
            'topic': 'Science',
            'account': '@DiscoverMag'
        },
        # Music
        {
            'topic': 'Music',
            'account': '@SpinninRecords'
        },
        {
            'topic': 'Music',
            'account': '@RollingStone'
        },
        {
            'topic': 'Music',
            'account': '@billboard'
        },
        # Sport
        {
            'topic': 'Sport',
            'account': '@NYDNSports'
        },
        {
            'topic': 'Sport',
            'account': '@SkySportsNews'
        },
        {
            'topic': 'Sport',
            'account': '@BBCSport'
        },
        # Politics
        {
            'topic': 'Politics',
            'account': '@nytpolitics'
        },
        {
            'topic': 'Politics',
            'account': '@CNNPolitics'
        },
        {
            'topic': 'Politics',
            'account': '@NBCPolitics'
        },
        # Tech
        {
            'topic': 'Tech',
            'account': '@TechCrunch'
        },
        {
            'topic': 'Tech',
            'account': '@ForbesTech'
        },
        {
            'topic': 'Tech',
            'account': '@thenextweb'
        },
        # Finance
        {
            'topic': 'Finance',
            'account': '@business'
        },
        {
            'topic': 'Finance',
            'account': '@CNNBusiness'
        },
        {
            'topic': 'Finance',
            'account': '@TheEconomist'
        },
        # Cinema
        {
            'topic': 'Cinema',
            'account': '@IMDb'
        },
        {
            'topic': 'Cinema',
            'account': '@netflix'
        },
        {
            'topic': 'Cinema',
            'account': "@THR"
        }
    ]
    return api, from_date, topic_channels

# Collect tweets
def collectTweets (api, from_date, topic_channels):
    for topic_channel in topic_channels:
         print(topic_channel['topic'] + ' ' + topic_channel['account'])
         topic = "from:" + topic_channel['account'] + " -filter:retweets"
         tweets = tw.Cursor(api.search, q=topic, lang="en", since=from_date, tweet_mode="extended").items(10000)
         attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]
         df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
         df['topic'] = topic_channel['topic']
         if not os.path.exists('../Tweets-csv/' + topic_channel['topic']):
             os.makedirs('../Tweets-csv/' + topic_channel['topic'])
         path = '../Tweets-csv/' + topic_channel['topic'] + '/' + topic_channel['account'] + '.csv'
         df.to_csv(path, index=None, header=True)

#Merge all CSV in one
def merge_tweets (topic_channels):
    list_of_files = []
    for topic_channel in topic_channels:
        path = '../Tweets-csv/' + topic_channel['topic'] + '/' + topic_channel['account'] + '.csv'
        list_of_files.append(path)
    result_obj = pd.concat([pd.read_csv(file) for file in list_of_files])
    result_obj.to_csv("../Tweets-csv/tweets.csv", index=None, header=True, encoding='utf-8-sig')

def getProfiles1 ():
    df = pd.DataFrame(columns=['text'])
    user = 'elonmusk'
    f = open("../Profiles/" + user + ".txt", "a", encoding="utf-8")
    try:
        for tweet in tw.Cursor(api.user_timeline, screen_name=user, exclude_replies=True, count=10).items():
            tweet_text = tweet.text
            time = tweet.created_at
            tweeter = tweet.user.screen_name
            tweet_dict = {"tweet_text": tweet_text.strip()}
            tweet_json = json.dumps(tweet_dict)
            df = df.append({'text': tweet_text}, ignore_index=True)
            print(df)
        path = "../Profiles/" + user + ".csv"
        df.to_csv(path, index=None, header=True)
    except tw.TweepError:
        time.sleep(60)

def getProfiles ():
    df = pd.DataFrame(columns=['text'])
    user = 'elonmusk'
    topic = "from:" + user
    tweets = tw.Cursor(api.user_timeline, screen_name=user, exclude_replies=True, tweet_mode="extended", count=10).items()
    attributes = [[tweet.full_text] for tweet in tweets]
    df = pd.DataFrame(data=attributes, columns=['text'])
    if not os.path.exists("../Profiles/" + user):
        os.makedirs("../Profiles/" + user)
    path = "../Profiles/" + user + ".csv"
    df.to_csv(path, index=None, header=True)

#Main code
api, from_date ,topic_channels = setAttr()
print("Set config end")

#print("Collect tweets end")
#collectTweets(api, from_date, topic_channels)

#merge_tweets(topic_channels)
print("Merge tweets end")

getProfiles()