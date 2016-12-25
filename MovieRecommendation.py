__author__ = 'lancefernando'
"""This Movie Recommendation program utilizes collaborative filtering to recommend movies the user may enjoy. 
	Data used is original data from MovieLens. It will ask a user to rate 50 random movies on a scale 
	from 0 to 5 where the 0 value means that the user has not seen the movie. The ratings are stored as a vector. 
	This vector is then compared to other user ratings using two different similarity measurements:
	Cosine similarity and Jaccard similarity. The 5 most similar user vectors are then utilized to recommend 
	up to five different movies which are outputted to the console and as a text file. Movies that are recommended 
	must have be rated a 5 by the recorded similar user. """
import random

"""Function reads movie titles from a given movie file and adds each movie title
	to a list. List of movie titles is then returned."""
def readMovies(filename):

    moviefile = open(filename, 'r')
    movieList = []
    #creating empty movie list
    for line in moviefile:
        line = line.split('|')
        #using '|' as delimiter to split
        movieList.append(line[1])
    moviefile.close()
    return movieList

"""Function uses given list and asks user to rate each movie in list. Each rating is then written
	to the given filename."""
def profilemaker(filename, movieList):
    ratingArray = ['0'] * len(movieList) #number of movies
    randomMovies = random.sample(range(len(movieList)), 50) #Grabbing 50 random movies from list
    ratingString = ''
    print("Please create your profile by rating the following movies from 0 to 5 (1 being horrible, 5 being amazing and 0 if not watched): ")

    for movie in randomMovies:
        print(movieList[movie])
        rating = raw_input("Enter your rating: ")

        while(not(rating.isdigit()) or int(rating) not in range(0,6)):
        	rating = raw_input("Please enter a valid rating: ")

        ratingArray[movie] = str(rating)
        #ratingString += str(rating) + ' '
        print(' ')

    for each in ratingArray:
        ratingString += each + ' '

    f = open(filename, 'w')
    f.write(ratingString)
    f.close()

"""Function will read given rating profile and returns list of ratings"""
def readProfile(filename):

    f = open(filename, 'r')
    lines = f.readlines()
    ratings = lines[0]
    ratings = ratings.strip(' ')
    ratings = ratings.split(' ')

    for i in range(0, len(ratings)):
        ratings[i] = int(ratings[i])
    f.close()
    return ratings

"""Function creates a dictionary using given file. Each key is the user
	and the value is a list of with the movies rated at index 0 and a list of ratings at index 1.
	This dictionary is then returned.""" 
def movieRatings(filename):

    ratingDict ={}
    ratings = open(filename, 'r')
    for line in ratings:
        line = line.strip('\n')
        line = line.split('\t')
        if line[0] in ratingDict:
            #enters this statement if the user has rated
            #multiple movies
            templist = []
            for x in range(0, len(ratingDict[line[0]])):
                #loops for the length of the user's rating list
                templist.append(ratingDict[line[0]][x])
                #adds each rating to the temporary list
            templist.append([int(line[1]), int(line[2])])
            #enters the newest rating to temporary list
            ratingDict[line[0]] = templist
            #setting the value of the user in dictionary to full rating list
        else:

            ratingDict[line[0]] = [[int(line[1]), int(line[2])]]

            #If user is not in dictionary yet, this will add user
            #and the user's rating
    ratings.close()

    return ratingDict

"""Takes a vector of ratings (user1) and a list of lists with movie IDs and their respective ratings
	as user2 and returns the cosine similarity between users."""
def computeCosSim(user1, user2):
	dotProd = 0
	user2Prod = 0
	user1Prod = 0

	# Computing the dot product between user1 and user2 ratings
	for i in range(len(user2)):

		movieID = user2[i][0]
		rating = user2[i][1]

		dotProd += rating * user1[movieID - 1]

		user2Prod += rating **2 #computing the user2 dot product of itself

	# Computing the user1 dot product of itself
	for i in range(len(user1)):

		user1Prod += user1[i] **2

	return float(dotProd)/(float(user1Prod)*float(user2Prod))

"""Takes a vector of ratings (user1) and a list of lists with movie IDs and their respective ratings
	as user2 returns the jaccard similarity between users."""
def computeJacSim(user1, user2):

	intersection = 0
	union = len(user1) # this is true since len(user1) is the whole sample size of the movie list

	for i in range(len(user2)):

		movieID = user2[i][0]
		rating = user2[i][1]

		# Values count as intersection when both users rate the same movie as a 3 or greater
		if user1[movieID - 1] >= 3 and rating >=3:
			intersection += 1

	return float(intersection)/float(union)

"""Calls all previous functions and determine movies that the user should watch 
	by comparing their ratings to the ratings of
    other users. Movies that are recommended must have a rating of 5 b y the calculated
    similar users."""
def computeRecommendation(ratingFile, moviesFile, userFile, recCosFile, recJacFile):

    ratingDict = movieRatings(ratingFile)
    movieList = readMovies(moviesFile)
    profilemaker(userFile, movieList)
    userRatings = readProfile(userFile)

    cosFile = open(recCosFile, 'w')
    jacFile = open(recJacFile, 'w')

    top5ListCos = []
    top5ListJac = []
    #creating empty lists for top 5 compatible users

    recommendListCos = []
    recommendListJac = []
    #creating empty recommended movie lists

    #computing cosine and jaccard similarity values between the client and other users' movie ratings
    for user in ratingDict.keys():
        otherUsers = ratingDict[user]

        cosSim = computeCosSim(userRatings, otherUsers)

        jacSim = computeJacSim(userRatings, otherUsers)

        top5ListCos.append([cosSim, user])
        top5ListJac.append([jacSim, user])

    #sorting list in descending order to grab the users that are most similar to the client
    top5ListCos = sorted(top5ListCos, reverse = True)
    top5ListJac = sorted(top5ListJac, reverse = True)

    top5ListCos = top5ListCos[0:5]
    top5ListJac = top5ListJac[0:5]

    #Creating a list of recommended movies from the most similar users based on cosine similarity
    for sim in range(0, 5):
        key = top5ListCos[sim][1]
        movies = ratingDict[key]
        counter = 1
        for i in range(0, len(movies)):
            if counter <= 5:
                #allows each user to recommend no more than 5 movies
                if movies[i][1] == 5 and userRatings[movies[i][0]] == 0:
                    #if the user rated the movie 5 and I have not watched the movie yet
                    movieID = movies[i][0]
                    if movieList[movieID] not in recommendListCos:
                        #If movie title is not in list
                        recommendListCos.append(movieList[movieID])
                        counter += 1
            else:
                break

    #Creating a list of recommended movies from the most similar users based on jaccard similarity
    for sim in range(0, 5):
        key = top5ListJac[sim][1]
        movies = ratingDict[key]
        counter = 1
        for i in range(0, len(movies)):
            if counter <= 5:
                #allows each user to recommend no more than 5 movies
                if movies[i][1] == 5 and userRatings[movies[i][0]] == 0:
                    #if the user rated the movie 5 and I have not watched the movie yet
                    movieID = movies[i][0]
                    if movieList[movieID] not in recommendListJac:
                        #If movie title is not in list
                        recommendListJac.append(movieList[movieID])
                        counter += 1
            else:
                break

    #writing recommended lists to given files            
    for i in range(0, len(recommendListCos)):
        cosFile.write(recommendListCos[i] + '\n')
    cosFile.close()

    for i in range(0, len(recommendListJac)):
        jacFile.write(recommendListJac[i] + '\n')
    jacFile.close()

"""Asks client which similarity metric they prefer to have movies recommended by.
	returns 0 if client chooses cosine similarity or 1 for jaccard similarity."""
def getSimilarityType():

    print("Based on your ratings and others that have rated similarly we have created two lists in no particular order of movies for you to watch.")
    print("The two lists of recommendations were computed based on two different similarity metrics. \n")
    similarity = raw_input("Enter 0 to view movies based on the Cosine-Similarity metric or 1 for Jaccard-Similarity recommendations: ")

    while(not(similarity.isdigit()) or int(similarity) not in range(0,2)):
    	similarity = raw_input("Please enter a valid entry [0 or 1]: ")

	return int(similarity)

"""Prints movies line by line from a given file to the console."""
def printMoviesFromFile(filename):
	file = open(filename, 'r')
	for line in file:
		print(line)
	file.close()

"""Calls printMoviesFromFile() function to print a list of movies based on the similarity metric
	the client chooses."""
def printRecommendedMovies(file1, file2, simType):

	if simType == 0:
		print("Here are your recommendations based on Cosine similarity. \n")
		printMoviesFromFile(file1)

		response = raw_input("Would you also like to view recommended movies based on Jaccard similarity? Yes or No: ")
		if response.lower() == 'yes':
			printMoviesFromFile(file2)
	else:
		print("Here are your recommendations based on Jaccard similarity. \n")
		printMoviesFromFile(file2)

		response = raw_input("Would you also like to view recommended movies based on Cosine similarity? Yes or No: ")
		if response.lower() == 'yes':
			printMoviesFromFile(file1)

	print("Thank you!")

def main():

    computeRecommendation('movieRatings.txt', 'movies.txt', 'profile.txt', 'cosRecommendedMovies.txt', 'jacRecommendedMovies.txt')
        
    simType = getSimilarityType()

    printRecommendedMovies('cosRecommendedMovies.txt', 'jacRecommendedMovies.txt', simType)
    
main()

