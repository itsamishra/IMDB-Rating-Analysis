import sqlite3

def main():
	connection = sqlite3.connect("movies.db")
	cursor = connection.cursor()

	command = "ALTER TABLE ratingUrl ADD trueScore INTEGER;"
	cursor.execute(command)
	connection.commit()

	cursor.close()
	connection.close()


if __name__ == '__main__':
	main()