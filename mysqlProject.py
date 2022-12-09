import mysql.connector
import os


# host      = localhost if the demo is running the MySQL DB on the local machine
# otherwise, we will figure it out when the time comes
# user      = username (duh)
# password  = try to set up a secret file. we dont want our password pushed up into our git repo
# database  = im guessing esports is correct
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="esports"
)

## === MODIFY FUNCTIONS === ##
def modify_team():
    print_table('team')
    team_id = int(input('Select team_id to modify: '))
    print("=== Modify a team ===")
    team_name = input("Enter team name: ")
    query = (
        "UPDATE team SET team_name = %s WHERE team_id = %s;"
    )
    data = (team_name,team_id)
    execute_query(query,True,data)

def modify_tournament():
    #list the table
    print_table('tournament')
    tournament_id = int(input('Select tournament_id to modify '))
    print("=== Modify a tournament ===")
    name = input("Enter tournament name: ")
    state = input("Enter tournament state: ")
    city = input("Enter tournament city: ")
    address = input("Enter tournament street address: ")
    s_year = input("Enter tournament start year: ")
    s_month = input("Enter tournament start month: ")
    s_day = input("Enter tournament start day: ")
    query = (
        "UPDATE tournament SET tournament_name= %s, start_day= %s, start_month= %s, start_year= %s, street_address= %s, city= %s, state= %s "
        "WHERE tournament_id = %s;"
    )
    data = (name, s_day, s_month, s_year, address, city, state, tournament_id)
    execute_query(query,True,data)

## === ADD FUNCTIONS === ##
def add_team():
    print("=== Add a team ===")
    team_name = input("Enter team name: ")
    query = (
        "INSERT INTO team(team_name) VALUES ('%s');" % (team_name)
    )
    execute_query(query,False)

def add_tournament():
    print("=== Add a tournament ===")
    name = input("Enter tournament name: ")
    state = input("Enter tournament state: ")
    city = input("Enter tournament city: ")
    address = input("Enter tournament street address: ")
    s_year = input("Enter tournament start year: ")
    s_month = input("Enter tournament start month: ")
    s_day = input("Enter tournament start day: ")
    query = (
            "INSERT INTO tournament(tournament_name, start_day, start_month, start_year, street_address, city, state) "
             "VALUES (%s, %s, %s, %s, %s, %s ,%s);"
             )
    data = (name, s_day, s_month, s_year, address, city, state)
    execute_query(query,True,data)

## === DELETE FUNCTIONS === ##
def delete_team():
    print_table('team')
    team_id = int(input('Select team_id to delete: '))
    print("=== Delete a team ===")
    query = ("DELETE FROM team WHERE team_id = " + str(team_id) + ";")
    execute_query(query, False)

def delete_tournament():
    print_table('tournament')
    print("=== Delete a tournament ===")
    tournament_id = int(input('Select tournament_id to delete '))
    query = ("DELETE FROM tournament WHERE tournament_id = " + str(tournament_id) + ";")
    execute_query(query,False)

## === RETRIEVAL FUNCTIONS === ##

def print_table(table):
    query = ("SELECT * FROM " + table)
    mycursor = mydb.cursor()
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Print the result of the query
    print("Tables in " + table + ":")
    for row in result:
        print(row)

def list_tables():
    # Get a list of all tables in the database
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    tables = mycursor.fetchall()

    # Print the list of tables
    print("Tables:")
    for table in tables:
        print(table[0])

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

def test_query():
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

def execute_query(query,hasdata,data = ()):
    # Execute the query
    mycursor = mydb.cursor()
    if hasdata:
        mycursor.execute(query,data)

    else:
        mycursor.execute(query)
    mydb.commit()
    tables = mycursor.fetchall()

## === MENUS === ##

def mainMenu():
  os.system('clear') # Clear the screen
  print("=== Main Menu ===")
  print("-----------------")
  print("1. Edit entity tables")
  print("2. View table values")
  print("3. Debug")
  print("4. Exit")

def debug():
    while True:
        os.system('clear') # Clear the screen
        print("=== Debug Menu ===")
        print("------------------")
        print("1. List all tables")
        print("2. Describe a table")
        print("3. Execute a query")
        print("4. Back")
        choice = int(input("Enter your choice(1-4): "))
        # Handle the user's choice
        if choice == 1:
            list_tables() # List all tables
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 2:
            describe_table() # Describe a table
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 3:
            test_query() # Execute a query
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 4:
            return

def editMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== Edit Menu ===")
        print("-----------------")
        print("1. Tournaments")
        print("2. Games")
        print("3. Teams")
        print("4. Players")
        print("5. Back") 
        choice = int(input("Enter your choice(1-5): "))
        # Handle the user's choice
        if choice == 1:
            tournamentMenu() # List all tables
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 2:
            print("Not yet implemented.")
#            gameMenu() # Describe a table
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 3:
            teamMenu() # Execute a query
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 4:
            print("Not yet implemented.")
#            playerMenu()
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 5:
            return

def tournamentMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== Tournament Menu ===")
        print("-----------------------")
        print("1. Add a tournament")
        print("2. Modify a tournament")
        print("3. Delete a tournament")
        print("4. Back") 
        choice = int(input("Enter your choice(1-4): "))
        # Handle the user's choice
        if choice == 1:
            add_tournament()
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 2:
            modify_tournament()
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 3:
            delete_tournament()
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 4:
            return

def teamMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== Team Menu ===")
        print("-----------------")
        print("1. Add a team")
        print("2. Modify a team")
        print("3. Delete a team")
        print("4. Back") 
        choice = int(input("Enter your choice(1-4): "))
        # Handle the user's choice
        if choice == 1:
            add_team()
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 2:
            modify_team()
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 3:
            delete_team()
            input("Press enter to continue...") # Wait for the user to press enter
        elif choice == 4:
            return


# Create an infinite loop to show the menu and handle user input
while True:
  mainMenu()
  choice = int(input("Enter your choice (1-4): "))
  if choice == 1:
    print("Not yet implemented.")
    editMenu() # List all tables
    input("Press enter to continue...") # Wait for the user to press enter
  elif choice == 2:
    print("Not yet implemented.")
#    viewMenu() # Describe a table
    input("Press enter to continue...") # Wait for the user to press enter
  elif choice == 3:
    debug() # Execute a query
    input("Press enter to continue...") # Wait for the user to press enter
  elif choice == 4:
    break

# TODO: add functions from the google doc
# TODO: make all these functions user friendly. EX: on adding games, prompt the player for if they want to create a new roster, or use an existing one.
