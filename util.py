import datetime

# ==================================================================
# Rowan University, Data Quality and Web Text Mining Final Project
# Patrick Richeal, last modified 2019-09-24
# 
# util.py - Various utility functions
# ==================================================================

def log(text):
    now = datetime.datetime.now()
    print('[' + now.strftime("%I:%M:%S") + '] ' + text)