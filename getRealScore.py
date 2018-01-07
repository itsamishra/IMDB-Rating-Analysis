from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import sqlite3
import numpy as np

# Adds true score to db
def addScore(url, score):
	connection = sqlite3.connect("movies.db")
	cursor = connection.cursor()

	command = "UPDATE ratingUrl SET true_Score="+str(score)+" WHERE ratingUrl = '"+str(url)+"'"
	#print(command)
	cursor.execute(command)
	connection.commit()

	connection.close()

def main():
	dbScore = []

	# Creates connection to db and cursor
	connection = sqlite3.connect("movies.db")
	cursor = connection.cursor()

	# Loads data from db
	command = "SELECT * FROM ratingUrl"
	cursor.execute(command)

	# Gets "true" score by disregarding 1/10's and 10/10's
	while True:
		try:
			# Gets url (i.e  db key) and scores (2 to 9) from SQLite db
			data = cursor.fetchone()
			url = data[1]
			scores = np.array(list(data[3:11]))
			
			# If no scores for 2-8 exist, then ignores db row
			numVotes = scores.sum()
			if numVotes!=0:
				trueScore = 2*(scores[0]/numVotes)+3*(scores[1]/numVotes)+4*(scores[2]/numVotes)+5*(scores[3]/numVotes)+6*(scores[4]/numVotes)+7*(scores[5]/numVotes)+8*(scores[6]/numVotes)+9*(scores[7]/numVotes)
				dbScore.append([url, trueScore])

		# Triggered once we reach end of SQLite db
		except TypeError:
			break
	connection.close()

	for i in dbScore:
		#print(type(i[]))
		addScore(i[0], i[1])


if __name__ == '__main__':
	main()