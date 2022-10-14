#!/usr/bin/env python3
# encoding: utf-8
import sys
import re
import json
import pandas as pd

INDEX_NAME = 'ratings'

if len(sys.argv) != 3:
    print('Please provide the name of the movies and ratings input files')

movies_filename = sys.argv[1]
ratings_filename = sys.argv[2]

# title contains the name of the film and the year
# eg. Toy Story (1995)
pattern = re.compile(r'(.*) \((\d+)\)')

movies_df = pd.read_csv(movies_filename)
ratings_df = pd.read_csv(ratings_filename)

movies = {}

for index, row in movies_df.iterrows():
    movieId = int(row['movieId'])
    m = pattern.match(row['title'])
    if m:
        title = m.group(1)
        year = int(m.group(2))
    else:
        title = row['title']
        year = None
    genres = row['genres'].split('|')
    create = {"create": {"_index": INDEX_NAME, "_id": movieId}}
    movies[movieId] = {"movieId": movieId, "title": title, "year": year, "genres": genres}

for index, row in ratings_df.iterrows():
    userId = int(row['userId'])
    movieId = int(row['movieId'])
    rating = int(row['rating'])
    timestamp = int(row['timestamp'])
    create = {"create": {"_index": INDEX_NAME, "_id": f"{userId}-{movieId}"}}
    rating = {
        "userId": userId,
        "movieId": movieId,
        "title": movies[movieId]['title'],
        "year": movies[movieId]['year'],
        "genres": movies[movieId]['genres'],
        "rating": rating,
        "@timestamp": timestamp
    }
    print(json.dumps(create))
    print(json.dumps(rating))
