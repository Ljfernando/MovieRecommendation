# Movie Recommendation Program
This Movie Recommendation program utilizes collaborative filtering to recommend movies the user may enjoy. Data used is original data from MovieLens(link below). It will ask a user to rate 50 random movies on a scale from 0 to 5 where the 0 value means that the user has not seen the movie. The ratings are stored as a vector. This vector is then compared to other user’s ratings using two different similarity measurements: Cosine similarity and Jaccard similarity. The 5 most similar user vectors are then utilized to recommend up to five different movies which are outputted to the console and as a text file. Movies that are recommended must have been rated a 5 by the recorded similar user. Two lists of recommended movies are created based on the two different similarity metrics and both lists can then be viewed. 


### Similarity Metrics
**Cosine Similarity**:
~~~~~~~~~~~~~~~
This approach defines the similarity between two users x and y as:
sim(x,y) = (x . y)/ ||x|| * ||y|| where x and y are vectors and (.) represents the dot product.

Dot product of two vectors is the result of their linear combination.
ex. a <- [1, 0, 3]; b <- [2, 1, 1]
a.b = 1*2 + 0*1 + 3*1 = 2 + 0 + 3 = 5

||x|| represents the vector x ‘dotted’ with itself.
ex. a <- [1, 0, 3]
||a|| = 1^2 + 0 ^2 + 3^2 = 1 + 0 + 9 = 10

The similarity values will be bounded from [0:1] where larger values equate to a stronger similarity.
~~~~~~~~~~~~~~~


**Jaccard Similarity**: 
~~~~~~~~~~~~~~~
This approach defines the similarity between users x and y as:
sim(x,y) = (x ∩ y)/ (x ∪ y) where x and y are vectors.
∩ is the intersection between two sets. For this program, the vectors x and y intersect where the values as the same index are ≥ 3. This allows for rated movies to only count if they are more preferable than not (given a rating of 3 or greater). 

∪ is the union between the two sets. This value is the number of movies that could have possibly been rated. All movies are accounted for, regardless of whether or not it was watched and rated.

The similarity values will be bounded from [0:1] where larger values equate to a stronger similarity.
~~~~~~~~~~~~~~~


### Running The Program

Download all necessary txt files(‘movies.txt’ & movieRatings.txt’) and the ‘MovieRecommendation.py’ file. Simply run the python file using command ’python MovieRecommendation.py’ on command line or program of choice. You will then be asked to rate 50 random movies. Your rating profile will be saved in your current directory as ‘profile.txt’. The list of recommended movies will be saved as ‘cosRecommendedMovies.txt’ for movies recommended by the Cosine similarity metric and as ‘jacRecommendedMovies.txt’ for movies recommended by the Jaccard similarity metric.


### Files
**Python File**:
~~~~~~~~~~~~~~~~~
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

computeCosSim(user1, user2):
-Computes the cosine similarity value [0:1] 
-user1 is a vector of ratings from the user running program
-user2 is a list of lists of a single users movieID and rating
-Returns cosine similarity value

computeJacSim(user1, user2):
-Computes Jaccard similarity value [0:1]
-similar parameters as computeCosSim() method
-Returns Jaccard similarity value

computeRecommendation(ratingFile, moviesFile, userFile, recCosFile, recJacFile):
-Utilizes the dictionary of ratings and computes the cosine and jaccard similarity of each user to the original user
-Two lists of users based on their cosine similarity metric and jacquard similarity metric are created and sorted from 	greatest to least(most similar to least similar)
-The 5 most similar users are then analyzed to find at most five movies to recommend to the original user that they have not yet seen.
-Movies that are rated a 5 by the similar users are added to a recommendation list.
-Two separate lists of recommended movies based on their respective similarity metric are then written to the given text files.

getSimilarityType():
-Asks user for which similarity metric they prefer to use
-Returns 0 for Cosine similarity and 1 for Jaccard similarity

printMoviesFromFile(filename):
-Reads in given file of movies
-Prints each movie line by line to console

printRecommendedMovies(file1, file2, simType):
-Calls printMoviesFromFile() depending on simType value
-Then proceeds to ask if user would like to view recommended movies based on other metric

main():
-Calls computeRecommendation() method with given parameters for file names
-Then prints recommended movies to console based on the users choice of similarity type.
~~~~~~~~~~~~~~~~~


**Data Files:**
~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~

[Both data files can be downloaded here](http://grouplens.org/datasets/movielens/)

**Author: Lance Fernando**