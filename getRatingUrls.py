from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import sqlite3
import math

# Creates db and table if they don't already exist
def initiateDb():
	connection = sqlite3.connect("movies.db")
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS ratingUrl(Name TEXT, ratingUrl TEXT)")
	
	cursor.close()
	connection.close()

# Adds (name,url) to database
def insertDb(name, url):
	name = name.replace("'","''")
	connection = sqlite3.connect("movies.db")
	cursor = connection.cursor()
	command = "INSERT INTO ratingUrl VALUES ('" + str(name) + "','" + str(url) + "')"
	cursor.execute(command)
	connection.commit()

	cursor.close()
	connection.close()

# Adds 'numMovies' number of movies to database (1000 by default)
def main(numMovies):
	# Template of page containing most popular movies of 2017
	urlTemplate = "http://www.imdb.com/search/title?year=2017&page="

	# Creates db and table if they don't already exist
	initiateDb()

	
	maxPage = math.ceil(numMovies/50)
	for pageName in range(1,maxPage+1):
		pageUrl = urlTemplate + str(pageName)
		client = urlopen(pageUrl)
		pageHtml = client.read()


		# Parses HTML
		pageSoup = soup(pageHtml, "html.parser")

		# Gets all 50 movies in page
		movieList = pageSoup.findAll("div", {"class":"lister-item mode-advanced"})

		# Iterates over all movies on page
		for movie in movieList:
			# Gets url of movie's page
			movieData = movie.findAll("h3", {"class":"lister-item-header"})[0].findAll("a")[0]
			movieUrl = movieData["href"]
			movieName = movieData.text

			# Creates movie's rating url
			ratingsUrl = "http://www.imdb.com"
			for char in movieUrl:
				if char!="?":
					ratingsUrl = ratingsUrl + char
				else:
					ratingsUrl = ratingsUrl + "ratings"
					break

			#print(movieName, ratingsUrl)
			insertDb(movieName,ratingsUrl)


		client.close()

if __name__ == '__main__':
	main(1000)