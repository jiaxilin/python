#!/usr/bin/env python3.13
# trakt2letterboxd.py

import sys
import json
import csv
import os

from datetime import datetime
from dotenv import load_dotenv
from urllib.request import Request, urlopen
from itertools import count

load_dotenv()

API_KEY = os.getenv("API_KEY")

# parse arguments

# if args missing, prompt input

user = input()
list_type = input()

headers = {
    'Content-Type': 'application/json',
    'trakt-api-version': '2',
    'trakt-api-key': API_KEY
}

# urls
# history = https://api.trakt.tv/users/loljiaxi/history/movies?page=1
# watchlist = https://api.trakt.tv/users/loljiaxi/watchlist/movies/added

new_list = []
field_names = []
file_name = ""

match list_type:
    case "watchlist":
        print("generating watchlist")

        file_name = 'watchlist.csv'
        field_names = ['tmdbID', 'Title', 'Year']

        r = Request(f'https://api.trakt.tv/users/{user}/watchlist/movies/added', headers=headers)
        response_body = urlopen(r).read()

        if response_body:
            data = json.loads(response_body)

            # loop through list
            for movie in data:
                newObj = {
                    'tmdbID': movie["movie"]["ids"]["tmdb"],
                    'Title': movie["movie"]["title"],
                    'Year': movie["movie"]["year"]
                }

                # add row to csv
                new_list.append(newObj)

        else:
            print("err")

    case "history":
        print("generating history")

        file_name = 'history.csv'
        field_names = ['tmdbID', 'Title', 'Year', 'Rewatch', 'WatchedDate']
        pageLength = 10

        # infinite loop for dynamic pagination
        for currPage in count(0):
            r = Request(f'https://api.trakt.tv/users/{user}/history/movies?page=' + str(currPage + 1), headers=headers)
            response_body = urlopen(r).read()
            
            if response_body:
                print(f"data page: {currPage + 1}")
                data = json.loads(response_body)

                # if arr empty
                if not data:
                    break

                for movie in data:
                    newObj = {
                        'tmdbID': movie["movie"]["ids"]["tmdb"],
                        'Title': movie["movie"]["title"],
                        'Year': movie["movie"]["year"],
                        'Rewatch': 0,
                        'WatchedDate': movie["watched_at"]
                    }

                    # add row to csv
                    new_list.insert(0, newObj)
        
        unique = []
        for movie in new_list:
            if movie['tmdbID'] in unique:
                movie['Rewatch'] = 1
            else:
                unique.append(movie['tmdbID'])


# create csv file
with open(file_name, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    writer.writerows(new_list)

print("list saved:", file_name)
    
# print(new_list)

# watchlist csv format
# tmdbID,Title,Year

# history csv format
# tmdbID,Title,Year,Rewatch,WatchedDate