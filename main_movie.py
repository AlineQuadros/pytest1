

# import libraries

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import string

import plotly.plotly as py
import plotly.graph_objs as go


#!  import datasets MOVIE LENS
movielens_movies = pd.read_csv('movielens-20m-dataset/movie.csv', sep=',')
movielens_rating = pd.read_csv('movielens-20m-dataset/rating.csv', sep=',')
movielens_tag = pd.read_csv('movielens-20m-dataset/tag.csv', sep=',')


#!  inspect basic dataset structure 
movielens_tag.head()
movielens_tag.shape
movielens_tag = movielens_tag.drop(columns='timestamp')
movielens_tag = movielens_tag.drop(columns='userId')

# drop NAs  
movielens_tag = movielens_tag.dropna()
movielens_tag.nunique()




#! explore ==============  TAGS ===========================
#! the aim is to create a co-occurence matrix and network to find associations of tags

#TODO tags need a bit of cleaning up, there's a lot of silly symbols and case-letter issues
# quick replace all to lowercase letters
movielens_tag['tag'] = movielens_tag['tag'].str.lower()
movielens_tag.nunique()


# gets counts of movies per tag
movies_per_tag = movielens_tag[['movieId','tag']].groupby('tag', as_index=False).count()
movies_per_tag.columns = ['tag', 'movies_per_tag']
movies_per_tag['movies_per_tag'].describe()

# plot hist of most common tags 
tag_counts = movielens_tag['tag'].value_counts()
tag_counts[:20].plot(kind='bar', figsize=(10,5))

# get counts of tags per movies
tags_per_movie = movielens_tag[['movieId','tag']].groupby('movieId', as_index=False).count()
tags_per_movie.columns = ['movieId', 'tags_per_movie']
tags_per_movie['tags_per_movie'].describe()

# Delete tags that appeared in just a few movies
# find tags to be deleted from main dataset
g = movies_per_tag[movies_per_tag.movies_per_tag > 15]
# delete tags from dataset TAGS
movielens_tag = movielens_tag[movielens_tag.tag.isin(g.tag)]

# Delete movies that contained very few tags each
h = tags_per_movie[tags_per_movie.tags_per_movie > 10]
# delete movies from dataset MOVIES
movielens_movies = movielens_movies[movielens_movies.movieId.isin(h.movieId)]
# delete same movies from dataset TAGS
movielens_tag = movielens_tag[movielens_tag.movieId.isin(h.movieId)]

#create matrix presence/absence of TAGS per MOVIE
movielens_tag['count'] = 1 
movielens_tag.nunique()
tags_matrix = movielens_tag.pivot_table(values='count', index=['movieId'], columns="tag", fill_value=0)

#! pearson correlation
tags_corr = tags_matrix.corr()
tags_corr_lists =  tags_corr.stack()


tags_negative = tags_corr_lists[tags_corr_lists < 0])
tags_positive = tags_corr_lists[tags_corr_lists > 0.5]
tags_positive = tags_positive[tags_positive < 1]
tags_positive = tags_positive.to_frame()

# fix index names
tags_positive["tags"] = tags_positive.index
tags_positive["tags"] = tags_positive["tags"].astype("str")
temp2 = tags_positive["tags"].str.split(',', expand=True)
temp2.columns = ['tag1', 'tag2']
tags_positive = tags_positive.assign(tag1=temp2['tag1'])
tags_positive = tags_positive.assign(tag2=temp2['tag2'])
tags_positive = tags_positive.drop(columns='tags')

tags_positive.tag1 = tags_positive.tag1.str.replace('[{}]'.format(string.punctuation), '')
tags_positive.tag2 = tags_positive.tag2.str.replace('[{}]'.format(string.punctuation), '')

# visualize network of common co-ocurrences
# create list of NODES
nodes_pos["tag_id"] = list(range(1, tags_positive.tag1.nunique()))
nodes_pos["tag"] = tags_positive.tag1.unique()


#create dataframe of EDGES


#! ========================  explore GENRES ============================
#! the aim is to understand the flavour of each movie

#Split 'genres' into multiple columns
temp = movielens_movies['genres'].str.split('|', expand=True)

# count frequency of each meta_genre
genres_big_count = movielens_movies[['movieId','genres']].groupby('genres').count()
genres_big_count


# TODO with MOVIELENS dataset
# check if there's biases= same user gave the same score to all movies scored
# remove these biased users
# delete tags singletons and doubletons
