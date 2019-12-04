import util # random local util functions
import configparser
import requests
import re
from nltk.corpus import words

# ==================================================================
# Rowan University, Data Quality and Web Text Mining Final Project
# Patrick Richeal, last modified 2019-12-02
# 
# get_symbols.py - Retrieves stock ticker symbols and saves to file
#
#                                     runtime was aprox ~13 minutes
# ==================================================================

# get config data
util.log('Reading config data...')
config = configparser.ConfigParser()
config.read('config.ini')

# get list of stock symbols from iex
util.log('Retrieving stock symbols from IEX Cloud...')
response = requests.get(
    url = config['iex']['url'] + '/ref-data/symbols',
    params = { 'token': config['iex']['token'] }
)

# regex for alpha only
alpha_regex = re.compile('[^a-zA-Z]')

# setup array of additional ignored stock symbols
additional_words = ['keys', 'com', 'has', 'co', 'ive', 'info', 'wins', 'apps', 'tv', 'jobs', 'www', 'ceo', 'jan', 'usa', 'pays', 'jets', 'laws', 'usb', 'eyes', 'expo', 'cars', 'cia', 'dvd']

# open symbols file to write to
util.log('Opening symbols.txt file for writing to...')
symbols_file = open('symbols.txt', 'w+')

# loop through each symbol and see if we should write it to the symbols file
for symbol_obj in response.json():
    # make symbol into lowercase alpha only characters
    symbol = alpha_regex.sub('', symbol_obj['symbol']).lower()
    # write symbol to file if its not an english word
    if symbol not in words.words() and symbol not in additional_words:
        symbols_file.write(symbol + "\n")
        util.log('Added "' + symbol + '" symbol to symbols.txt')

util.log('Finished')

# close file
symbols_file.close()