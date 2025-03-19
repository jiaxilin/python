#!/usr/bin/env python3.13
# trakt2letterboxd.py

import sys
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
import os
from urllib.request import Request, urlopen

load_dotenv()

API_KEY = os.getenv("API_KEY")

# parse arguments

# if args missing, prompt input

user = 'loljiaxi'
listType = 'watchlist'

headers = {
    'Content-Type': 'application/json',
    'trakt-api-version': '2',
    'trakt-api-key': API_KEY
}

# urls
# history = https://api.trakt.tv/users/loljiaxi/history/movies
# watchlist = https://api.trakt.tv/users/loljiaxi/watchlist/movies/added

r = Request('https://api.trakt.tv/users/loljiaxi/watchlist/movies/added', headers=headers)

response_body = urlopen(r).read()

newlist = []

if response_body:
    # create csv file

    data = json.loads(response_body)

    # loop through list
    for movie in data:
        # check if movie already exists in array
        # exists = 'false'

        newObj = {
            'tmdbID': movie["movie"]["ids"]["tmdb"],
            'Title': movie["movie"]["title"],
            'Year': movie["movie"]["year"],
            'WatchedDate': ''
        }

        # add row to csv
        newlist.append(newObj)

    with open('watchlist.csv', 'w', newline='') as csvfile:
        fieldnames = ['tmdbID', 'Title', 'Year', 'WatchedDate']

        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(newlist)
        
    
    print(newlist)

    # save csv
else:
    print("err")

# watchlist csv format
# tmdbID,Title,Year

# history csv format
# tmdbID,Title,Year,Rewatch,WatchedDate