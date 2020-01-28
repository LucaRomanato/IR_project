import os
import pandas as pd
import tweepy as tw

#Script used for Tweets scraping

consumer_key = 'pw0eWIQgm02PNGCEwt8dmEMSE'
consumer_secret_key = 'IU18kd20PPhjZlanc3eE2S1DEgXARUr3DQpOFmAu11ErbNQcj1'
access_token = '1126373990883319808-LdRh3RjseJK6mhduC16vHLtX65tWvB'
access_token_secret = 'froKBiFQbDOtl0OrmFWIUu6N5PaWGJRAixFQON8dMnZjd'

auth = tw.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)