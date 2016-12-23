__author__ = 'lancefernando'
import random
## Function reads movie titles from a given movie file and adds each movie title
## to a list 

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

## Function uses given list and asks user to rate each movie in list and stores each
## rating into given filename
def profilemaker(filename, movieList):
    ratingArray = ['0'] * 1682 #number of movies
    randomMovies = random.sample(range(1,len(movieList)), 50)
    ratingString = ''
    print("Please create your profile by rating the following movies from 0 to 5 (0 if not watched): ")
    for movie in randomMovies:
        #iterates over first 50 movies
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

##    Function will read given rating profile and returns list
##    of ratings
def readProfile(filename):

    f = open(filename, 'r')
    lines = f.readlines()
    ratings = lines[0]
    ratings = ratings.strip(' ')
    #removing any extra white space on ends
    ratings = ratings.split(' ')
    for i in range(0, len(ratings)):
        ratings[i] = int(ratings[i])
    f.close()
    return ratings

##     """Function creates a dictionary using given file. Each key is the user
##    and the value is the user's rating and movie rated"""   
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

def dotProduct(user1, user2):
	dotProd = 0

	for rating in range(len(user1)):
		dotProd += user1[rating] * user2[rating]

	return dotProd


def computeRecommendation(ratingFile, moviesFile, userFile, recommendedFile):
    """Function will call all previous functions and determine movies
    that the user should watch by comparing their ratings to the ratings of
    other users. Movies that are recommended must have a rating of 5 by the calculated
    similar users."""
    ratingDict = movieRatings(ratingFile)
    movieList = readMovies(moviesFile)
    profilemaker(userFile, movieList)
    userRatings = readProfile(userFile)
    file = open(recommendedFile, 'w')
    top5List = []
    #creating empty list for top 5 compatible users
    recommendList = []
    #creating empty recommended movie list for

    selfProduct = dotProduct(userRatings, userRatings)#dot product of user ratings with itself

    for user in ratingDict.keys():
        value = ratingDict[user]

        compatibleSum = 0
        #using summation variable to compute dot product

        otherSelfProd = 0 # dot product of other users with themselves

        for i in range(0, len(value)):
            movieNum = value[i][0]
            rating = value[i][1]
            compatibleSum += userRatings[movieNum-1] * rating 
            #incorporating dot product by multiplying personal rating to user's rating
            #cumulating each product to test compatibility

            otherSelfProd += rating**2 #computing dot product of itself
        cosineSim = float(compatibleSum)/ float(selfProduct * otherSelfProd)
        top5List.append([cosineSim, user])
    top5List = sorted(top5List, reverse = True)
    #sorting list in reverse from largest to smallest
    top5List = top5List[0:5]

    #list becomes the top 5 similar users
    for sim in range(0, 5):
        key = top5List[sim][1]
        movies = ratingDict[key]
        counter = 1
        for i in range(0, len(movies)):
            if counter <= 5:
                #allows each user to recommend no more than 5 movies
                if movies[i][1] == 5 and userRatings[movies[i][0]] == 0:
                    #if the user rated the movie 5 and I have not watched the movie yet
                    movieID = movies[i][0]
                    if movieList[movieID] not in recommendList:
                        #If movie title is not in list
                        recommendList.append(movieList[movieID])
                        counter += 1
            else:
                break
    for i in range(0, len(recommendList)):
        file.write(recommendList[i] + '\n')
    file.close()
    return recommendList

def main():
    recommendList = computeRecommendation('movieRatings.txt', 'movies.txt', 'profile.txt', 'recommendedMovies.txt')
    print('Based on your ratings and others that have rated similarly we have created a list in no particular order of movies for you to watch:')
    for each in recommendList:
        print(each)
    
main()

