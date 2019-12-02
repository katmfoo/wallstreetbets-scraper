import util # random local util functions
import configparser
import praw # reddit sdk
import re

# ==================================================================
# Rowan University, Data Quality and Web Text Mining Final Project
# Patrick Richeal, last modified 2019-12-02
# 
# subreddit_scrape.py - Scrapes the desired subreddit for mention
#     of stock ticker symbols and gathers data about frequency/time
#     of mention
# ==================================================================

# get config data
util.log('Reading config data...')
config = configparser.ConfigParser()
config.read('config.ini')

# TODO: load symbols into symbols variable from symbols.txt

# function to find any stock symbol in given string
def get_symbol_matches(text):
    for symbol in symbols:
        result = re.search('[ .,]+' + symbol + '[ .,]+', text)
        if result != None:
            print(result)

# initialize reddit sdk / subreddit object
reddit = praw.Reddit(
    client_id=config['reddit']['client_id'],
    client_secret=config['reddit']['client_secret'],
    user_agent=config['reddit']['user_agent']
)
subreddit = reddit.subreddit('wallstreetbets')

for submission in subreddit.new(limit=100):
    print(submission.title)
    get_symbol_matches(submission.title + ' ' + submission.selftext)