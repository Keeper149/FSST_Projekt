import sqlite3

# Path to your .db file
db_path = r"C:\Users\Max\Documents\Schule\4CHEL\FSST\Spotify_Website_Projekt\ORM\selftest.db"

# Connect to the database
connection = sqlite3.connect(db_path)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Example: Retrieve all rows from a table named 'your_table'
table_name = 'people'
query = f"SELECT * FROM {table_name}"

try:
    cursor.execute(query)
    rows = cursor.fetchall()

    # Print the retrieved data
    for row in rows:
        print(row)
except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Close the connection
connection.close()
