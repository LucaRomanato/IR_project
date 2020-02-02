import os
import pandas as pd
import tweepy as tw


# Set twitter api kei and parameter varius
def setAttr():
    consumer_key = '5p1yWHj3oaCqPbWqvQRZVMHl6'
    consumer_secret_key = 'KigvCscRtl24NhKnT61KVbTG7MbM7d7qGKVcNpgNKRaBzZJs5H'
    access_token = '1126373990883319808-ny24fJVmhg9SiKEofKUVsmPHlN1AWT'
    access_token_secret = 'P9qo9szpw2fQyhwU2uqZf9ku6frs0st27GyMfKtjkLAtK'

    auth = tw.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    from_date = "2020-01-01"
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
def collectTweets(api, from_date, topic_channels):
    tutto = pd.DataFrame(columns=['user', 'text', 'location', 'date'])
    for topic_channel in topic_channels:
        print(topic_channel['topic'] + ' ' + topic_channel['account'])
        tweets = tw.Cursor(api.user_timeline, screen_name=topic_channel['account'], lang="en", since="2019-11-24",
                           until="2020-01-30", tweet_mode="extended").items(10000)
        attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in
                      tweets]
        df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
        df['topic'] = topic_channel['topic']
        tutto = tutto.append(df)
    tutto.to_csv(r'../Tweet-csv/tutto-csv.csv', index=None, header=True)


# Get profile
def getProfiles(api):
    user = 'elonmusk'
    tweets = tw.Cursor(api.user_timeline, screen_name=user, exclude_replies=True, tweet_mode="extended",
                       count=10).items()
    attributes = [[tweet.full_text] for tweet in tweets]
    df = pd.DataFrame(data=attributes, columns=['text'])
    if not os.path.exists("../Profiles/" + user):
        os.makedirs("../Profiles/" + user)
    path = "../Profiles/" + user + ".csv"
    df.to_csv(path, index=None, header=True)


# Main code
def twitter_scraper():
    api, from_date, topic_channels = setAttr()
    print("Set config end")

    collectTweets(api, from_date, topic_channels)
    print("Collect tweets end")

    getProfiles()
    print("Collect profile tweet end")
