from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import sqlite3

# Adds weighed score to db
def addScore(url, score):
	connection = sqlite3.connect("movies.db")
	cursor = connection.cursor()

	command = "UPDATE ratingUrl SET weighedScore="+str(score)+" WHERE ratingUrl IS '"+str(url)+"'"
	#print(command)
	cursor.execute(command)
	connection.commit()

	connection.close()

# Gets weighed score from websites rating page
def main():
	# Creates connection to db and cursor
	connection = sqlite3.connect("movies.db")
	cursor = connection.cursor()

	# Loads data from db
	command = "SELECT * FROM ratingUrl"
	cursor.execute(command)

	# Gets all urls
	ratingUrl = []
	while True:
		try:
			url = cursor.fetchone()[1]
			ratingUrl.append(url)
		except:
			break

	# Iterates over all ratings in db
	for ratingPage in ratingUrl:
		#ratingPage = "http://www.imdb.com/title/tt6487416/ratings"

		# Gets url html
		client = urlopen(ratingPage)
		ratingHtml = client.read()

		# Parses html
		pageSoup = soup(ratingHtml, "html.parser")

		# Try-catch statement makes sure movies with no ratings have null weighed score
		try:
			weighedScore = float(pageSoup.findAll("div", {"name":"ir"})[0].findAll("span")[0].text)
		except:
			continue

		print(weighedScore)

		# Sets Weighed Score in db
		addScore(ratingPage, weighedScore)

# Calls main()
if __name__ == '__main__':
	main()