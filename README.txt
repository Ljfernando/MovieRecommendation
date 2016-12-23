This program utilizes collaborative filtering to recommend movies the user may enjoy. It will ask a user to rate 50 random movies on a scale from 0 to 5 where the 0 value means that the user has not seen the movie. The ratings are stored as a vector. This vector is then compared to other user’s ratings using a cosine similarity measurement to measure the similarity between users. The 5 most similar user vectors are then utilized to recommend up to five different movies which are outputted to the console and as a text file. Movies that are recommended must have be rated a 5 by the recorded similar user. 

In order to run this program, download all necessary txt files and the MovieRecommendation.py file. Simply run the python file using python MovieRecommendation.py on your command line. You will then be asked to rate 50 random movies. Your rating profile will be saved in your current directory as ‘profile.txt’. The list of recommended movies will be saved as ‘recommendedMovies.txt’

————————————
Files
————————————

~~~~~~~~~~~~~
Python File:
MovieRecommendation.py
Methods:
readMovies(filename):
-Takes in the text file of movies to create an array of all the movies. 
-The index of the movie is based on the movie ID - 1 since indexing begins at 0.
-Returns array of movies

profileMaker(filename,movieList):
-Creates a profile(vector) of movie ratings.
-Movies rated are randomly selected from moveList array.
-This vector is written to a text file designated as filename.

readProfile(filename):
-Takes in a given file of a single users ratings.
-Returns an array of the users ratings

movieRatings(filename):
-Takes in a given file of movie ratings.
-The file is split to read line by line
-Each line is added to a dictionary where the key is the user number
-The value is a 2D list where the first column is the movie ID and the second is the user’s rating of that movie
-Returns the dictionary

dotProduct(user1, user2):
-Computes the cosine similarity of two vectors: user1 and user2 
-Returns this value

computeRecommendation(ratingFile, moviesFile, userFile, recommendedFile):
-Utilizes the dictionary of ratings and computes the cosine similarity of each user to the original user
-A list of users based on their cosine similarity metric is created and sorted from greatest to least(most similar to least similar)
-The 5 most similar users are then analyzed to find at most five movies to recommend to the original user that they have not yet seen.
-Movies that are rated a 5 by the similar users are added to a recommendation list.
-List of recommended movies is returned and a written to the given text file.

main():
-Calls computeRecommendation(’movieRatings.txt', 'movies.txt', 'profile.txt’, ‘recommendedMovies.txt’)
-Prints recommended movies to console.

Data Files:

movies.txt
-Text file of different movie attributes separated by ‘|’. 
-First index contains the movie ID
-Second index is the movie title
-Other attributes are ignored

movieRatings.txt
-Text file of over 100k different ratings for movies mentioned in the ‘movies.txt’ file
-First index is the user ID
-Second index is the movie ID
-Third index is the user’s rating of the movie
-Other attributes are ignored

Both data files downloaded from http://grouplens.org/datasets/movielens/
~~~~~~~~~~~~~~~~~~~~
Author: Lance Fernando

 