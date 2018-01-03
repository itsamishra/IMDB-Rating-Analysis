from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import sqlite3

# Adds number of people per rating to the db
def addOneToTenRatings(url, rating):
	connection = sqlite3.connect("movies.db")
	cursor = connection.cursor()

	command = "UPDATE ratingUrl SET Ten="+str(rating[0])+",Nine="+str(rating[1])+",Eight="+str(rating[2])+",Seven="+str(rating[3])+",Six="+str(rating[4])+",Five="+str(rating[5])+",Four="+str(rating[6])+",Three="+str(rating[7])+",Two="+str(rating[8])+",One="+str(rating[9])+" WHERE ratingUrl IS '"+str(url)+"'"
	cursor.execute(command)
	connection.commit()

	connection.close()

# Gets # of ratings for each entry in database
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

	connection.close()

	# Iterates over all ratings in db
	for ratingPage in ratingUrl:
		# Gets url html
		client = urlopen(ratingPage)
		ratingHtml = client.read()

		# Parses html
		pageSoup = soup(ratingHtml, "html.parser")
		ratings = pageSoup.findAll("div", {"class":"leftAligned"})
		
		# Deals with edge case in which page has no ratings
		if len(ratings)==0:
			addOneToTenRatings(ratingPage, [0,0,0,0,0,0,0,0,0,0])
			continue

		# Creates list containing # of people who game movie each rating (1 to 10)
		eachRating = []
		for i in range(1,11):
			eachRating.append(ratings[i].text.strip().replace(",",""))

		# Adds rating to db
		addOneToTenRatings(ratingPage, eachRating)

if __name__ == '__main__':
	main()