# pytest1
Predicting scores of movies that don't exist yet


Hi there!
Would you like to write a very original movie?
By very original I mean "plot" that has never been used before.
But writing such an original movie has its dangers, right? 
What if you could predict how well this movie will perform just by analysing the plot and a few 
other features?

Here I used the TMDB 5000 dataset to extract keywords and features of movies that have been scored (0 to 10) by thousands of users worldwide.
The plots are assembled based on a network analysis of the most frequent combinations of keywords used to describe each movie.

simmilarly, a network analisys can tell you the combinations of keywords that have never been used before.
Then, we add other features such as director, studio, budget, ect. to describe the movies

Using machine learning and classification algorithms, the final score is predicted as 
""amazing", "very good", "good", "average", "bad", "very bad", or "horrible".

Finally, the tree classifier is used with the new combination of keywords and features,
to predict how the new movie will perform: 
  - scores
  - revenue
  - popularity

