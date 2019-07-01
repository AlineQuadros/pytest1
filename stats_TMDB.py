# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:06:16 2019

@author: MyLAP
"""

# import libraries

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split 
from sklearn import metrics
from sklearn import svm

#!  import datasets TMDB
tmdb_movies = pd.read_csv('tmdb-5000-movie-dataset/tmdb5000movies.csv', sep=',')

# subset continuous variables
tmdb_num = tmdb_movies.loc[:,['budget', 'popularity', 'revenue', 'runtime', 'vote_average', 'vote_count']]
tmdb_num.hist()
# replace 0 with NaN
tmdb_num = tmdb_num.replace({ 0:np.nan})

# correlation matrix
cor = tmdb_num.corr()

# cute corr plot
ax = sns.heatmap(cor, vmin=-1, vmax=1, center=0, cmap=sns.diverging_palette(20, 220, n=200), square=True)

# plot
plt.scatter(tmdb_num["budget"], tmdb_num["revenue"],  alpha=0.5)
plt.show()

# ----------------CLASSIFICATION TREES -------------------------

keys_per_movie = gg
# filter top 100
keys_per_movie = keys_per_movie[keys_per_movie["value"].isin(top_100key["keyword"])]
#create matrix presence/absence of KEYWORDS per MOVIE
keyw100_matrix = keys_per_movie.pivot_table(values='count', index=['movieId'], columns="value", fill_value=0)
keyw100_matrix["id"] = keyw100_matrix.index

# join average_score
ready100 = pd.merge(keyw100_matrix, tmdb_movies, how='left', on='id')
ready100 = ready100.drop(columns=['status', 'tagline', 'keywords'])
# create average_score as category rounding numbers
ready100['score_cat'] = pd.to_numeric(ready100['vote_average']).round(0).astype(int)
# create 5-scale category based on vote_average
#ready100['movie_eval'] = "amazing"
#ready100.movie_eval[ready100.vote_average<=7.9] = "good"
#ready100.movie_eval[ready100.vote_average<=6.9] = "okish"
#ready100.movie_eval[ready100.vote_average<=5.9] = "bad"
#ready100.movie_eval[ready100.vote_average<=3.9] = "very bad"
#ready100.movie_eval.value_counts()

ready100['movie_eval'] = "amazing"
ready100.movie_eval[ready100.vote_average<=7.8] = "very good"
ready100.movie_eval[ready100.vote_average<=7.0] = "good"
ready100.movie_eval[ready100.vote_average<=6.3] = "average"
ready100.movie_eval[ready100.vote_average<=5.7] = "bad"
ready100.movie_eval[ready100.vote_average<=4.5] = "very bad"
ready100.movie_eval[ready100.vote_average<=3.9] = "horrible"
ready100.movie_eval.value_counts()

# steps from datacamp https://www.datacamp.com/community/tutorials/decision-tree-classification-python

#split dataset in features and target variable
feature_cols = top_100key.keyword
X = ready100[feature_cols] # Features
possible_y = ['score_cat','movie_eval']

# only 2 movies classified as 1 - change to 0 otherwise stratified sampling wont work
ready100.score_cat[ready100.score_cat==1] = 0
ready100.score_cat[ready100.score_cat==9] = 10

# classification tree        
for j in possible_y:
    y = ready100[possible_y[j]] # Target variable
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, stratify=y, random_state=1) 
    clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)
    clf = clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    
# regression tree        
#for j in possible_y:
#    y = ready100[possible_y[j]] # Target variable
#    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) 
#    clf = DecisionTreeRegressor(max_depth=3)
#    clf = clf.fit(X_train,y_train)
#    y_pred = clf.predict(X_test)
#    print("R2:",metrics.r2_score(y_test, y_pred))
#    print("Error:",metrics.mean_squared_error(y_test, y_pred))


# ---------------- Support Value Machines  ------------------------
clf = svm.SVC(gamma='scale', decision_function_shape='ovo')
clf.fit(X, y) 
y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Report:",metrics.classification_report(y_test, y_pred))


# -------------predict SCORES of new movie plot -------------------
