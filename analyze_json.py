import json
import util # random local util functions
import datetime
import requests
import configparser

# ==================================================================
# Rowan University, Data Quality and Web Text Mining Final Project
# Patrick Richeal, last modified 2019-12-06
# 
# analyze_json.py - Reads in symbol_mentions.json and retrieves
#     stock prices for highly mentioned stock symbols for each week
# ==================================================================

# get config data
util.log('Reading config data...')
config = configparser.ConfigParser()
config.read('config.ini')

# returns a datetime for the friday of the given week and year
def get_friday_of_week(week_number, year='2018'):
    d = str(year) + "-W" + str(week_number)
    r = datetime.datetime.strptime(d + '-5', "%Y-W%W-%w")#.strftime('%Y-%m-%d')
    return r

# retrieves the stock price for the given stock at the given datetime
def get_stock_price_at(symbol, datetime):
    date_value = datetime.strftime('%Y%m%d')
    response = requests.get(
        url = config['iex']['url'] + '/stock/' + symbol + '/chart/date/' + date_value,
        params = { 'token': config['iex']['token'], 'chartByDay': True }
    )
    # print(symbol + ' - ' + date_value)
    # # print(response.json())
    # print(response.json()[0]['close'])

    if response.json():
        return str(response.json()[0]['close'])
    else:
        return "No price data"

# load in symbol_mentions.json file
util.log('Loading symbol_mentions.json...')
symbol_mentions_file = open('symbol_mentions.json', 'r')
symbol_mentions = json.load(symbol_mentions_file)
symbol_mentions_file.close()

util.log('Displaying stock price data for significant mentions in weeks...')

# for each week
for week in symbol_mentions:
    # get week array
    week_array = symbol_mentions[week]

    # get highest and second highest mentioned symbols
    highest_mentioned_symbol = week_array[0]
    second_highest_mentioned_symbol = week_array[1]

    # if the highest mentioned symbol was mentioned more than 1.5 times the second highest,
    # its significant enough to look at
    if highest_mentioned_symbol['mentions'] > (second_highest_mentioned_symbol['mentions'] * 1.5):
        # get highest mentioned symbol
        symbol = highest_mentioned_symbol['symbol']

        # print info about the week and symbol
        print('Week ' + str(week) + ' - highest mentioned symbol "' + symbol + '" (mentions: ' + str(highest_mentioned_symbol['mentions']) + ', sentiment score: ' + str(highest_mentioned_symbol['sentiment_score']) + ')')

        # get the date of the friday of given week
        friday_of_week_date = get_friday_of_week(week)

        # based on that friday, get the stock price for the 2 weeks around that friday (before and after)
        two_weeks_prior_date = friday_of_week_date - datetime.timedelta(weeks=2)
        one_week_prior_date = friday_of_week_date - datetime.timedelta(weeks=1)
        one_week_after_date = friday_of_week_date + datetime.timedelta(weeks=1)
        two_weeks_after_date = friday_of_week_date + datetime.timedelta(weeks=2)

        # get stock prices for each date
        two_weeks_prior_price = get_stock_price_at(symbol, two_weeks_prior_date)
        one_week_prior_price = get_stock_price_at(symbol, one_week_prior_date)
        friday_of_week_price = get_stock_price_at(symbol, friday_of_week_date)
        one_week_after_price = get_stock_price_at(symbol, one_week_after_date)
        two_weeks_after_price= get_stock_price_at(symbol, two_weeks_after_date)

        # print price data for each date
        print('\t2 weeks prior\t' + two_weeks_prior_price)
        print('\t1 week prior\t' + one_week_prior_price)
        print('\tWeek ' + str(week) + '\t\t' + friday_of_week_price)
        print('\t1 week after\t' + one_week_after_price)
        print('\t2 weeks after\t' + two_weeks_after_price)