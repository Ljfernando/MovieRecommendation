__author__ = 'lancefernando'
"""This Movie Recommendation program utilizes collaborative filtering to recommend movies the user may enjoy. 
	Data used is original data from MovieLens. It will ask a user to rate 50 random movies on a scale 
	from 0 to 5 where the 0 value means that the user has not seen the movie. The ratings are stored as a vector. 
	This vector is then compared to other user ratings using three different similarity measurements:
	Cosine similarity, Jaccard similarity and Pearson Correlation Coefficient. The 5 most similar user vectors are then utilized to recommend 
	up to five different movies which are outputted to the console and as a text file. Movies that are recommended 
	must have be rated a 5 by the recorded similar user. """
import random
import math


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
    print("Please create your profile by rating the following movies from 0 to 5 (1 being horrible, 5 being amazing and 0 if not watched):\n")

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

	return float(dotProd)/(math.sqrt(float(user1Prod))*math.sqrt(float(user2Prod)))


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


"""Takes a vector of ratings (user1) and a list of lists with movie IDs and their respective ratings
    as user2 returns the Pearson Correlation Coefficient between users. Calls computeMean in order
    to """
def computePccSim(user1, user2, user1Mean):
    dotProd = 0
    user2Prod = 0
    user1Prod = 0

    user2Mean = 0

    # Computing the mean of user2s ratings
    for i in range(len(user2)):
        rating = user2[i][1]
        user2Mean += rating

    user2Mean = float(user2Mean)/float(len(user2))

    # Computing the dot product between user1 and user2 ratings
    for i in range(len(user2)):

        movieID = user2[i][0]
        rating = float(user2[i][1])

        dotProd += float((rating - user2Mean) * (float(user1[movieID - 1]) - user1Mean))

        user2Prod += float((rating - user2Mean) **2) #computing the user2 dot product of itself

    # Computing the user1 dot product of itself
    for i in range(len(user1)):

        user1Prod += float((float(user1[i]) - user1Mean) **2)

    return float(dotProd)/(math.sqrt(float(user1Prod))*math.sqrt(float(user2Prod)))


"""Computes the mean of a given vector of ratings and returns this value"""
def computeMean(user1):

    mean = 0

    for i in range(len(user1)):
        mean += user1[i]
    return(float(mean)/float(len(user1)))


"""Calls all previous functions and determine movies that the user should watch 
	by comparing their ratings to the ratings of
    other users. Movies that are recommended must have a rating of 5 by the
    similar users."""
def computeRecommendation(ratingFile, moviesFile, userFile, recCosFile, recJacFile, recPccFile):

    ratingDict = movieRatings(ratingFile)
    movieList = readMovies(moviesFile)
    profilemaker(userFile, movieList)
    userRatings = readProfile(userFile)

    cosFile = open(recCosFile, 'w')
    jacFile = open(recJacFile, 'w')
    pccFile = open(recPccFile,'w')

    #creating empty lists for top 5 compatible users
    top5ListCos = []
    top5ListJac = []
    top5ListPcc = []

    #creating empty recommended movie lists
    recommendListCos = []
    recommendListJac = []
    recommendListPcc = []

    #computing mean of client ratings to use for PCC
    userMean = computeMean(userRatings)


    #computing cosine and jaccard similarity values between the client and other users' movie ratings
    for user in ratingDict.keys():
        otherUsers = ratingDict[user]

        cosSim = computeCosSim(userRatings, otherUsers)

        jacSim = computeJacSim(userRatings, otherUsers)

        pccSim = computePccSim(userRatings, otherUsers, userMean)

        top5ListCos.append([cosSim, user])
        top5ListJac.append([jacSim, user])
        top5ListPcc.append([pccSim, user])

    #sorting list in descending order to grab the users that are most similar to the client
    top5ListCos = sorted(top5ListCos, reverse = True)
    top5ListJac = sorted(top5ListJac, reverse = True)
    top5ListPcc = sorted(top5ListPcc, reverse = True)

    top5ListCos = top5ListCos[0:5]
    top5ListJac = top5ListJac[0:5]
    top5ListPcc = top5ListPcc[0:5]

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


    #Creating a list of recommended movies from the most similar users based on PCC
    for sim in range(0, 5):
        key = top5ListPcc[sim][1]
        movies = ratingDict[key]
        counter = 1
        for i in range(0, len(movies)):
            if counter <= 5:
                #allows each user to recommend no more than 5 movies
                if movies[i][1] == 5 and userRatings[movies[i][0]] == 0:
                    #if the user rated the movie 5 and I have not watched the movie yet
                    movieID = movies[i][0]
                    if movieList[movieID] not in recommendListPcc:
                        #If movie title is not in list
                        recommendListPcc.append(movieList[movieID])
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

    for i in range(0, len(recommendListPcc)):
        pccFile.write(recommendListPcc[i] + '\n')
    pccFile.close()   


"""Prints movies line by line from a given file to the console."""
def printMoviesFromFile(filename):
	file = open(filename, 'r')
	for line in file:
		print(line)
	file.close()


"""Calls printMoviesFromFile() function to print a list of movies based on the similarity metric
	the client chooses."""
def printRecommendedMovies(file1, file2, file3):

    print("Based on your ratings and others that have rated similarly we have created three lists of movies in no particular order for you to watch.")
    print("The three lists of recommendations were computed based on three different similarity metrics. \n")
    print("Enter C to view movies based on the Cosine-Similarity metric.")
    print("Enter J to view movies based on the Jaccard-Similarity metric.")
    simType = raw_input("Enter P to view movies based on the Pearson Correlation Coefficient metric.\n").lower().strip()


    while simType != "q":

    	if simType == "c":
            print("Here are your recommendations based on Cosine similarity. \n")
            printMoviesFromFile(file1)
            
            print("Would you also like to view recommended movies based on the other similarity metrics?")
            print("Enter J to view movies based on the Jaccard-Similarity metric.")
            print("Enter P to view movies based on the Pearson Corellation Coefficient metric.")

            simType = raw_input("Enter Q to quit.\n").lower().strip()


    	elif simType == "j":
            print("Here are your recommendations based on Jaccard similarity. \n")
            printMoviesFromFile(file2)

            print("Would you also like to view recommended movies based on the other similarity metrics?")
            print("Enter C to view movies based on the Cosine-Similarity metric.")
            print("Enter P to view movies based on the Pearson Corellation Coefficient metric.")
            simType = raw_input("Enter Q to quit.\n").lower().strip()

        elif simType == "p":
            print("Here are your recommendations based on the Pearson Correlation Coefficient.\n")
            printMoviesFromFile(file3)

            print("Would you also like to view recommended movies based on the other similarity metrics?")
            print("Enter C to view movies based on the Cosine-Similarity metric.")
            print("Enter J to view movies based on the Jaccard-Similarity metric.")
            simType = raw_input("Enter Q to quit.\n").lower().strip()

        else:
            print("Not a valid entry.")
            print("Enter C to view movies based on the Cosine-Similarity metric.")
            print("Enter J to view movies based on the Jaccard-Similarity metric.")
            print("Enter P to view movies based on the Pearson Correlation Coefficient metric.")
            simType = raw_input("Enter Q to quit.\n").lower().strip()

    print("Thank you and enjoy!")


def main():

    computeRecommendation('movieRatings.txt', 'movies.txt', 'profile.txt', 'cosRecommendedMovies.txt', 'jacRecommendedMovies.txt', 'pccRecommendedMovies.txt')

    printRecommendedMovies('cosRecommendedMovies.txt', 'jacRecommendedMovies.txt', 'pccRecommendedMovies.txt')
    
main()

