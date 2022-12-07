import mysql.connector
import os
from secret import password

# host      = localhost if the demo is running the MySQL DB on the local machine 
# otherwise, we will figure it out when the time comes
# user      = username (duh) 
# password  = try to set up a secret file. we dont want our password pushed up into our git repo
# database  = im guessing esports is correct
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=password,
  database="esports"
)

# Create a function to show the main menu
def show_menu():
  os.system('clear') # Clear the screen
  print("MySQL Command Line Interface")
  print("----------------------------")
  print("1. List all tables")
  print("2. Describe a table")
  print("3. Execute a query")
  print("4. Exit")

# Create a function to list all tables in the database
def list_tables():
  # Get a list of all tables in the database
  mycursor = mydb.cursor()
  mycursor.execute("SHOW TABLES")
  tables = mycursor.fetchall()

  # Print the list of tables
  print("Tables:")
  for table in tables:
    print(table[0])

# Create a function to describe a table in the database
def describe_table():
  # Ask the user to enter the name of the table
  table_name = input("Enter the name of the table: ")

  # Get the description of the table
  mycursor = mydb.cursor()
  mycursor.execute("DESCRIBE " + table_name)
  description = mycursor.fetchall()

  # Print the description of the table
  print("Table Description:")
  for col in description:
    print(col[0], col[1], col[2])

# Create a function to execute a query
def execute_query():
  # Ask the user to enter the query to execute
  query = input("Enter the query to execute: ")

  # Execute the query
  mycursor = mydb.cursor()
  mycursor.execute(query)
  result = mycursor.fetchall()

  # Print the result of the query
  print("Query Result:")
  for row in result:
    print(row)

# Create an infinite loop to show the menu and handle user input
while True:
  show_menu() # Show the main menu
  choice = int(input("Enter your choice: ")) # Ask the user to enter their choice

  # Handle the user's choice
  if choice == 1:
    list_tables() # List all tables
    input("Press enter to continue...") # Wait for the user to press enter
  elif choice == 2:
    describe_table() # Describe a table
    input("Press enter to continue...") # Wait for the user to press enter
  elif choice == 3:
    execute_query() # Execute a query
    input("Press enter to continue...") # Wait for the user to press enter
  elif choice == 4:
    break # Exit the program



# TODO: add functions from the google doc
# TODO: make all these functions user friendly. EX: on adding games, prompt the player for if they want to create a new roster, or use an existing one. 

# https://www.w3schools.com/python/python_mysql_getstarted.asp
