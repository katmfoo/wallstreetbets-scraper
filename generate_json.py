import util # random local util functions
import datetime
import json

# ==================================================================
# Rowan University, Data Quality and Web Text Mining Final Project
# Patrick Richeal, last modified 2019-12-07
# 
# generate_json.py - Translates the symbol_mentions.csv file into a
#     dictionary like file that shows the score of each symbol for
#     each week in the year
# ==================================================================

# Load symbol mentions from symbol_mentions.txt file
util.log('Loading symbol mentions from symbol_mentions.csv...')
symbol_mentions_file = open('symbol_mentions.csv', 'r')
symbol_mentions = symbol_mentions_file.read().splitlines()
symbol_mentions_file.close()

# open symbol mentions json file to write to
util.log('Opening symbol_mentions.json file for writing to...')
symbol_mentions_file = open('symbol_mentions.json', 'w+')

# create dictionary object to hold symbol frequencies by week number
data_obj = {}

# for each mention
for mention in symbol_mentions:
    # get the various values from the line
    values = mention.split(',')
    timestamp = int(values[0])
    stock_symbol = values[1]
    sentiment = int(values[2])

    week_number = str(datetime.datetime.fromtimestamp(timestamp).isocalendar()[1])

    # create week number dictionary if doesn't exist
    if not data_obj.get(week_number):
        data_obj[week_number] = []

    # initialize stock object in week array if it doesn't exist
    if not any(stock_obj.get('symbol', None) == stock_symbol for stock_obj in data_obj[week_number]):
        data_obj[week_number].append({
            'symbol': stock_symbol,
            'mentions': 0,
            'sentiment_score': 0
        })
    
    # increment mentions and add to sentiment score for appropriate stock object in week number list
    for stock_obj in data_obj[week_number]:
        if stock_obj['symbol'] == stock_symbol:
            stock_obj['mentions'] += 1
            stock_obj['sentiment_score'] += sentiment


# sort stock objects in week number lists by mentions
for week_list in data_obj.items():
    data_obj[week_list[0]] = sorted(week_list[1], key = lambda i: i['mentions'], reverse=True)

# dump dictoinary object to json file
symbol_mentions_file.write(json.dumps(data_obj, sort_keys=True, indent=2))

# close file
symbol_mentions_file.close()