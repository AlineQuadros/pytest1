# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:22:50 2019

@author: MyLAP
"""

# import libraries

import numpy as np
import pandas as pd
import string
from scipy.stats import spearmanr


#!  import datasets TMDB
tmdb_movies = pd.read_csv('tmdb-5000-movie-dataset/tmdb5000movies.csv', sep=',')
#tmdb_cred = pd.read_csv('tmdb-5000-movie-dataset/tmdb5000credits.csv', sep=',')
oscar = pd.read_csv('oscar_dataset.csv', sep=',')

# subsetting  - GET KEYWORDS
tmdb_key = tmdb_movies.loc[:, ["id", "keywords"]]
# subsetting  - GET CREW
tmdb_crew = tmdb_cred.loc[:, ["id", "crew"]]

# remove empty strings
tmdb_key["keywords"].replace('[]', np.nan, inplace=True)
tmdb_key = tmdb_key.dropna()

# explore JSON structure of keywords
print(tmdb_key.loc[1:3, "keywords"])
# remove puctuation - this is SOO silly - i cant parse JSON
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace('[','')
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace(']','')
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace('{','')
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace('}','')
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace('id','')
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace('name','')
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace('\": ','')
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace(' \"','')
tmdb_key["keywords"] = tmdb_key["keywords"].str.replace('\"','')

keyw = tmdb_key["keywords"].str.split(',', expand=True)

# drop id columns
for i in range(0, 194, 2):
    keyw = keyw.drop([i], axis = 1)
    
# get movie id from original dataset
keyw["movieId"] = tmdb_key["id"]

# melt dataframe of keywords per movie_ID
gg = keyw.melt(id_vars=['movieId'])
gg = gg.drop(columns='variable')
gg["movieId"].nunique()

#TODO there are numbers instead of keywords in several records/ remove them
# trim, remove puctuation
gg["value"] = gg["value"].str.strip()
gg["value"] = gg["value"].str.replace('[{}]'.format(string.punctuation), '')

#gg[gg["value"].isnumeric()] = ""

# number of unique keywords
gg["value"].nunique()
# remove Nones
#gg = gg[gg.loc[:, "value"] is  None]

# plot hist of most common keywords 
kc = gg['value'].value_counts()
kc[:20].plot(kind='bar', figsize=(10,5))

# 100 commonest keywords
top_100key = kc[:100].to_frame()
top_100key['keyword'] = top_100key.index
top_150key = kc[:150].to_frame()
top_150key['keyword'] = top_150key.index

#create matrix presence/absence of KEYWORDS per MOVIE
gg['count'] = 1 
keyw_matrix = gg.pivot_table(values='count', index=['movieId'], columns="value", fill_value=0)
keyw_matrix.index = keyw["movieId"]

#! spearman correlation
rho, pval = spearmanr(keyw_matrix)
# adjust column names
rho_dt = pd.DataFrame(data=rho[0:,0:], index=keyw_matrix.columns, columns=keyw_matrix.columns)

# make upper diagonal as NaN to get rid of them ans stack dataframe
rho_dt.values[np.triu_indices_from(rho_dt, 0)] = np.nan
rho_dt = rho_dt.stack()
rho_dt = rho_dt.to_frame()

# save dataset
rho_dt.to_csv(r'rho_dataset.csv')

