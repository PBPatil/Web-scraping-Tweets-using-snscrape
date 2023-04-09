
# !pip install tweepy
# !pip install snscrape
%reset -f

import snscrape.modules.twitter as snstwitter
import pandas as pd
from tqdm import tqdm
query = "Fantasy Premier League OR FPL until:2023-04-09 since:2012-01-01"
tweets = []
limit = 100


for tweet in snstwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.id,tweet.date,tweet.username, tweet.content,
                       tweet.hashtags,tweet.retweetCount,tweet.likeCount,
                       tweet.replyCount,tweet.source,
                       tweet.user.location,tweet.user.verified,
                       tweet.user.followersCount,tweet.user.friendsCount])
        
df = pd.DataFrame(tweets, columns=['ID','Timestamp','User','Text',
                                   'Hashtag','Retweets','Likes',
                                   'Replies','Source',
                                   'Location','Verified_Account',
                                   'Followers','Following'])
df.to_csv("FPL_Tweets1.csv",index=False)
# print(df) 

#############################################################################
%reset -f
import snscrape.modules.twitter as snstwitter
import pandas as pd
from tqdm import tqdm

# Define the start and end dates
start_date = pd.Timestamp('2012-01-01')
end_date = pd.Timestamp('now').floor('D')

# Define the query string
query = "Fantasy Premier League OR FPL since:{} until:{}".format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

# Define the number of tweets to collect per year
limit = 10000

# Define an empty list to store the tweets
tweets = []

# Loop over each year
for year in range(start_date.year, end_date.year+1):
    # Define the start and end dates for the current year
    year_start_date = pd.Timestamp('{}-01-01'.format(year))
    year_end_date = pd.Timestamp('{}-12-31'.format(year))

    # Define the query string for the current year
    year_query = "{} since:{} until:{}".format(query, year_start_date.strftime('%Y-%m-%d'), year_end_date.strftime('%Y-%m-%d'))

    # Loop over each tweet for the current year
    for tweet in tqdm(snstwitter.TwitterSearchScraper(year_query).get_items()):
        if len(tweets) >= limit*(year-start_date.year+1):
            break
        else:
            tweets.append([tweet.id,tweet.date,tweet.username, tweet.content,
                           tweet.hashtags,tweet.retweetCount,tweet.likeCount,
                           tweet.replyCount,tweet.source,
                           tweet.user.location,tweet.user.verified,
                           tweet.user.followersCount,tweet.user.friendsCount])

# Create a DataFrame from the list of tweets
df = pd.DataFrame(tweets, columns=['ID','Timestamp','User','Text',
                                   'Hashtag','Retweets','Likes',
                                   'Replies','Source',
                                   'Location','Verified_Account',
                                   'Followers','Following'])
# extract year and month into new columns
df['Year'] = df['Timestamp'].dt.year
df['Month'] = df['Timestamp'].dt.strftime('%b-%y').astype('str')

df.to_csv("FPL_tweets.csv",index=False)
# df['Month'].value_counts()
df['Year'].value_counts()
