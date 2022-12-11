import mysql.connector
import os
from tabulate import tabulate
import string
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

# TODO: add function to check for valid entries

## =========================== MODIFY FUNCTIONS ============================== ##

def modify_player():
    print("=== Modify a player ===")
    retrieval_query("SELECT * FROM player")
    player_id = int(input('Select player_id to modify: '))
    print("=== Current values ===")
    retrieval_query("SELECT * FROM player WHERE player_id = " + str(player_id) + ";")
    in_game_name = input("Enter player in game name: ")
    retrieval_query("SELECT * FROM team")
    team_id = int(input('Select player team (-1 if no team) '))
    first_name = input("Enter player first name ")
    last_name = input("Enter player last name ")
    start_year = input("Enter the players first year ")
    start_month = input("Enter the players first month ")
    start_day = input("Enter the players first day ")
    if team_id == -1:
        query = (
            "UPDATE player SET in_game_name = %s, first_name = %s, last_name = %s, start_day = %s, start_month = %s, start_year = %s "
            "WHERE player_id = %s;"
        )
        data = (in_game_name, first_name, last_name, start_day, start_month, start_year, player_id)
    else:
        query = (
            "UPDATE player SET in_game_name = %s, team_id = %s, first_name = %s, last_name = %s, start_day = %s, start_month = %s, start_year = %s "
            "WHERE player_id = %s;"
        )
        data = (in_game_name, team_id, first_name, last_name, start_day, start_month, start_year, player_id)
    execute_query(query,True,data)

def modify_team():
    retrieval_query("SELECT * FROM team")
    team_id = int(input('Select team_id to modify: '))
    print("=== Modify a team ===")
    team_name = input("Enter team name: ")
    query = (
        "UPDATE team SET team_name = %s WHERE team_id = %s;"
    )
    data = (team_name,team_id)
    execute_query(query,True,data)

def modify_tournament():
    print("=== Modify a tournament ===")
    retrieval_query("SELECT * FROM tournament")
    tournament_id = int(input('Select tournament_id to modify '))
    print("=== Current values ===")
    retrieval_query("SELECT * FROM tournament WHERE tournament_id = " + str(tournament_id) + ";")
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

def complete_game(tournament_id):
    print("=== Complete an unfinished game ===")
    not_empty = retrieval_query("SELECT * FROM game WHERE tournament_id = " + str(tournament_id) + " AND winner_team_id IS NULL;")
    if not not_empty:
        input("This table is empty!")
    else:
        game_id = int(input("Enter the game_id of the game you would like to complete: "))

        mycursor = mydb.cursor()
        duration = int(input("Enter the duration of the game in minutes: "))
        query = ("SELECT team_id, team_name FROM team JOIN game ON team_id = team_1_id OR team_id = team_id_2 WHERE game_id = " + str(game_id) + ";")
        retrieval_query(query)
        winner = input('Enter team_id of the team that won the game: ')
        query = (
            "INSERT INTO game (duration,winner_team_id) "
            "VALUES (%s, %s);"
        )
        data = (duration, winner)
        mycursor.execute(query,data)
        roster_team_1_id = retrieve_attr_val("game", game_id, "team_1_roster_id")
        roster_team_2_id = retrieve_attr_val("game", game_id, "team_2_roster_id")

        add_game_participants(game_id, roster_team_1_id, roster_team_2_id)


def modify_game(tournament_id):
    print("=== Modify a game ===")
    complete_game = int(input("Enter 1 if you would like to modify a completed game, 2 if you want to modify an incomplete game: "))
    if complete_game == 1:
        not_empty = retrieval_query("SELECT * FROM game WHERE tournament_id = " + str(tournament_id) + " AND winner_team_id IS NOT NULL;")
    else:
        not_empty = retrieval_query("SELECT * FROM game WHERE tournament_id = " + str(tournament_id) + " AND winner_team_id IS NULL;")
    if not not_empty:
        input("This table is empty!")
    else:
        game_id = int(input("Enter the game_id of the game you would like to modify: "))
        print("=== Current values ===")
        retrieval_query("SELECT * FROM game WHERE game_id = " + str(game_id) + ";")

        old_roster_ids = (retrieve_attr_val("game_id", game_id, "team_1_roster_id"), retrieve_attr_val("game_id", game_id, "team_2_roster_id"))
        retrieval_query("SELECT * FROM team")
        team_id_1 = int(input('Enter the first team_id that should participate: '))
        team_id_2 = int(input('Enter the second team_id that should participate: '))
        query_team_1 = ("SELECT * FROM roster WHERE team_id = "+str(team_id_1)+ ';')
        retrieval_query(query_team_1)
        roster_team_1_id = int(input("Enter roster_id for team 1: "))
        query_team_2 = ("SELECT * FROM roster WHERE team_id = " +str(team_id_2)+ ';')
        retrieval_query(query_team_2)
        roster_team_2_id = int(input("Enter roster_id for team 2: "))

        if not (roster_team_1_id in old_roster_ids) or not (roster_team_2_id in old_roster_ids):
            query = "DELETE FROM game_participant WHERE game_id = " + str(game_id) + ";"
            execute_query(query, False)

        start_time = int(input("Enter game start time (military time, no colon): "))
        start_day = int(input("Enter game start day: "))
        start_month = int(input("Enter game start month: "))
        start_year = int(input("Enter game start year: "))

        if complete_game != 1:
            query = (
                "INSERT INTO game (tournament_id,team_1_id,team_2_id,team_1_roster_id,team_2_roster_id,start_time,start_day,start_month,start_year,duration,winner_team_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s);"
            )
            data = (tournament_id,team_id_1,team_id_2,roster_team_1_id,roster_team_2_id,start_time,start_day,start_month,start_year)
            execute_query(query,True,data)
        else:
            mycursor = mydb.cursor()
            duration = int(input("Enter the duration of the game in minutes: "))
            query = ("SELECT team_id, team_name FROM team WHERE team_id = " + str(team_id_1) + " OR team_id = " + str(team_id_2) + ";")
            retrieval_query(query)
            winner = input('Enter team_id of the team that won the game: ')
            query = (
                "INSERT INTO game (tournament_id,team_1_id,team_2_id,team_1_roster_id,team_2_roster_id,start_time,start_day,start_month,start_year,duration,winner_team_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s);"
            )
            data = (tournament_id, team_id_1, team_id_2, roster_team_1_id, roster_team_2_id, start_time, start_day, start_month, start_year, duration, winner)
            mycursor.execute(query,data)
            game_id = mycursor.lastrowid


            add_game_participants(game_id, roster_team_1_id, roster_team_2_id)

## =========================== ADD FUNCTIONS =========================== ##
def add_game_participants(game_id, team_1_roster_id, team_2_roster_id):
    mycursor = mydb.cursor()
    query = (
        "SELECT player_id, in_game_name, team_name, first_name, last_name "
        "FROM ("
            "SELECT * FROM (SELECT * FROM roster WHERE roster_id = " + str(team_1_roster_id) + " OR roster_id = " + str(team_2_roster_id) + ") RL "
            "NATURAL JOIN roster_member) R "
        "NATURAL JOIN ("
            "SELECT team_name, player_id, in_game_name, first_name, last_name "
            "FROM player NATURAL JOIN team) P;"
    )
    mycursor.execute(query)
    result = mycursor.fetchall()
    column_names = mycursor.column_names
    header_list = []
    # Print the result of the query
    for name in column_names:
        name = name.replace('_', ' ')
        name = string.capwords(name)
        header_list.append(name)
    for row in result:
        print(tabulate([row], headers=header_list, tablefmt="github"))
        kills = int(input('Enter the number of kills the player got this game: '))
        deaths = int(input('Enter the number of deaths today the player got this game: '))
        query_game_part = ("INSERT INTO game_participant (game_id,player_id,kills,deaths) VALUES (%s, %s, %s, %s)")
        data = (game_id,row[0],kills,deaths )
        execute_query(query_game_part,True,data)

def add_roster(team_id):
    mycursor = mydb.cursor()
    print("=== Create a roster ===")
    query ="SELECT * FROM player WHERE team_id = "+str(team_id)+";"
    retrieval_query(query)
    print("Rosters are comprised of three players")
    player_1_id = int(input("Enter player_id for the first player: "))
    player_2_id = int(input("Enter player_id for the second player: "))
    player_3_id = int(input("Enter player_id for the third player: "))
    query = (
        "INSERT INTO roster (team_id ) VALUES ("+str(team_id)+");"
    )
    mycursor.execute(query, False)
    player1_query = (
            "INSERT INTO roster_member (roster_id,player_id ) VALUES (%s, %s);"
    )
    player1_data = (mycursor.lastrowid, player_1_id)

    player2_query = (
            "INSERT INTO roster_member (roster_id,player_id ) VALUES (%s, %s);"
    )
    player2_data = (mycursor.lastrowid, player_2_id)

    player3_query = (
            "INSERT INTO roster_member (roster_id,player_id ) VALUES (%s, %s);"
    )
    player3_data = (mycursor.lastrowid,player_3_id)

    execute_query(player1_query,True,player1_data)
    execute_query(player2_query, True, player2_data)
    execute_query(player3_query, True, player3_data)
    
def add_player():
    print("=== Add a new player ===")
    in_game_name = input("Enter player's in game name: ")
    retrieval_query("SELECT * FROM team")
    team_id = int(input('Select player team (-1 if no team): '))
    first_name = input("Enter the player's real first name: ")
    last_name = input("Enter player last name: ")
    start_year = input("Enter the year the player started playing professionally: ")
    start_month = input("Enter the player's first month: ")
    start_day = input("Enter the players first day: ")
    if team_id == -1:
        query = (
            "INSERT INTO player(in_game_name, first_name, last_name, start_day, start_month, start_year) "
            "VALUES (%s, %s, %s, %s, %s, %s ,%s);"
        )
        data = (in_game_name, first_name, last_name, start_day, start_month, start_year)
    else:
        query = (
            "INSERT INTO player(in_game_name, team_id, first_name, last_name, start_day, start_month, start_year) "
            "VALUES (%s, %s, %s, %s, %s, %s ,%s);"
        )
        data = (in_game_name, team_id, first_name, last_name, start_day, start_month, start_year)
    execute_query(query,True,data)
    

def add_sponsor():
    print("=== Add a sponsor ===")
    retrieval_query("SELECT * FROM team")
    sponsor_name_team_id = int(input("Enter the team_id that this sponsor is supporting: "))
    sponsor_name = input("Enter sponsor name: ")
    query = (
        "INSERT INTO sponsor(sponsor_name,sponsored_team_id) VALUES (%s, %s);"
    )
    data = (sponsor_name,sponsor_name_team_id)
    execute_query(query,True,data)

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
    s_day = input("Enter the day of the month the tournament starts: ")
    s_month = input("Enter tournament start month (numerical): ")
    s_year = input("Enter tournament start year: ")
    address = input("Enter the street address of the venue the tournament will take place at: ")
    city = input("Enter tournament city: ")
    state = input("Enter tournament state (two leter abbreviation): ")
    query = (
            "INSERT INTO tournament(tournament_name, start_day, start_month, start_year, street_address, city, state) "
             "VALUES (%s, %s, %s, %s, %s, %s ,%s);"
             )
    data = (name, s_day, s_month, s_year, address, city, state)
    execute_query(query,True,data)

def add_team_to_tournament():
    print("=== Add a team to a tournament ===")
    retrieval_query("SELECT * FROM tournamnet")
    tournament_id = int(input('Select tournament_id to add a team to '))
    retrieval_query("SELECT * FROM team")
    team_id = int(input('Select team_id to add to the tournament '))
    query = (
            "INSERT INTO tournament_participant(tournament_id, team_id) "
            "VALUES (%s, %s)"
            )
    data = (tournament_id, team_id)
    execute_query(query,True,data)

def add_game(tournament_id):
    print("=== Add a game ===")
    retrieval_query("SELECT * FROM team")
    team_id_1 = int(input('Enter the first team_id that should participate: '))
    team_id_2 = int(input('Enter the second team_id that should participate: '))
    query_team_1 = ("SELECT * FROM roster WHERE team_id = "+str(team_id_1)+ ';')
    retrieval_query(query_team_1)
    roster_team_1_id = int(input("Enter roster_id for team 1: "))
    query_team_2 = ("SELECT * FROM roster WHERE team_id = " +str(team_id_2)+ ';')
    retrieval_query(query_team_2)
    roster_team_2_id = int(input("Enter roster_id for team 2: "))
    start_time = int(input("Enter game start time (military time, no colon): "))
    start_day = int(input("Enter game start day: "))
    start_month = int(input("Enter game start month: "))
    start_year = int(input("Enter game start year: "))
    finished_game = int(input('Enter 1 if this game has yet to be played or 2 if this game has already been played: '))

    if finished_game == 1:
        query = (
            "INSERT INTO game (tournament_id,team_1_id,team_2_id,team_1_roster_id,team_2_roster_id,start_time,start_day,start_month,start_year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        )
        data = (tournament_id,team_id_1,team_id_2,roster_team_1_id,roster_team_2_id,start_time,start_day,start_month,start_year)
        execute_query(query,True,data)
    else:
        mycursor = mydb.cursor()
        duration = int(input("Enter the duration of the game in minutes: "))
        query = ("SELECT team_id, team_name FROM team WHERE team_id = " + str(team_id_1) + " OR team_id = " + str(team_id_2) + ";")
        retrieval_query(query)
        winner = input('Enter team_id of the team that won the game: ')
        query = (
            "INSERT INTO game (tournament_id,team_1_id,team_2_id,team_1_roster_id,team_2_roster_id,start_time,start_day,start_month,start_year,duration,winner_team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s);"
        )
        data = (tournament_id, team_id_1, team_id_2, roster_team_1_id, roster_team_2_id, start_time, start_day, start_month, start_year, duration, winner)
        mycursor.execute(query,data)
        game_id = mycursor.lastrowid

        add_game_participants(game_id, roster_team_1_id, roster_team_2_id)

## =========================== DELETE FUNCTIONS =========================== ##

def delete_item(table_name):
    print("=== Delete a", table_name, "===")
    retrieval_query("SELECT * FROM " + table_name)
    id = input("Enter the id of the item you would like to delete: ")
    query = ("DELETE FROM " + table_name + " WHERE " + table_name + "_id = " + str(id) + ";")
    execute_query(query, False)

def delete_sponsor():
    print("=== Delete a sponsor ===")
    retrieval_query("SELECT * FROM sponsor")
    sponsor_team_id = input("Enter your sponsors team_id: ")
    query = ("DELETE FROM sponsor WHERE sponsored_team_id = " + str(sponsor_team_id) + ";")
    execute_query(query, False)

## =========================== RETRIEVAL FUNCTIONS =========================== ##

def get_value(message, integer=False, constraints=[]):
    valid = False
    sql_substrings = [
        ';', ')', '(', ','
    ]

    while not valid:
        if integer:
            result = int(input(message))
        else:
            result = input(message)
        # put all new constraints here
        condition_list = [
            integer and result < 0,
            
            "TIME" in constraints and result > 2400,
            "STATE" in constraints and len(result) > 2,

        ]
        for ss in sql_substrings : condition_list.append(ss in str(result))

        if False in condition_list:
            print("Invalid input, please try again (ctrl+C to quit the program)")
        else:
            valid = True


    return result

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

    result = execute_query(query,False)

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
    return tables

def retrieval_query(query):
    mycursor = mydb.cursor()
    mycursor.execute(query)
    result = mycursor.fetchall()
    column_names = mycursor.column_names
    header_list = []
    # Print the result of the query
    for name in column_names:
        name = name.replace('_', ' ')
        name = string.capwords(name)
        header_list.append(name)
    print(tabulate(result, headers=header_list, tablefmt="github"))
    return len(result) != 0

def retrieve_attr_val(table, tuple_id, attr_name):
  mycursor = mydb.cursor()
  if table in { "game", "player", "team", "tournament", "roster" }:
    mycursor.execute("SELECT " + attr_name + " FROM " + table + " WHERE " + table + "_id = " + str(tuple_id) + ";")
    result = mycursor.fetchall()
    return result[0][0]
        
## =========================== EDIT MENUS =========================== ##

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
        choice = int(input("Enter your choice: "))
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
        else:
            return

def editMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== Edit Menu ===")
        print("-----------------")
        print("1. Tournaments")
        print("2. Games")
        print("3. Teams")
        print("4. Sponsors")
        print("5. Players")
        print("6. Roster")
        print("7. Back") 
        choice = int(input("Enter your choice: "))
        # Handle the user's choice
        if choice == 1:
            tournamentMenu() # List all tables
        elif choice == 2:
            gameMenu() # Describe a table
        elif choice == 3:
            teamMenu() # Execute a query
        elif choice == 4:
            sponsorMenu() # Execute a query
        elif choice == 5:
            playerMenu()
        elif choice == 6:
            rosterMenu()
        else:
            return

def tournamentMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== Tournament Menu ===")
        retrieval_query("SELECT * FROM tournament")
        print("-----------------------")
        print("1. Add a tournament")
        print("2. Modify a tournament")
        print("3. Delete a tournament")
        print("4. Back") 
        choice = int(input("Enter your choice: "))
        # Handle the user's choice
        if choice == 1:
            add_tournament()
        elif choice == 2:
            modify_tournament()
        elif choice == 3:
            delete_item("tournament")
        else:
            return

def teamMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== Team Menu ===")
        retrieval_query("SELECT * FROM team")
        print("-----------------")
        print("1. Add a team")
        print("2. Change team name")
        print("3. Delete a team")
        print("4. Back") 
        choice = int(input("Enter your choice: "))
        # Handle the user's choice
        if choice == 1:
            add_team()
        elif choice == 2:
            modify_team()
        elif choice == 3:
            delete_item("team")
        else:
            return

def sponsorMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== Sponsor Menu ===")
        retrieval_query("SELECT * FROM sponsor")
        print("--------------------")
        print("1. Add a sponsor")
        print("2. Delete a sponsor")
        print("3. Back") 
        choice = int(input("Enter your choice: "))
        # Handle the user's choice
        if choice == 1:
            add_sponsor()
        elif choice == 2:
            delete_sponsor()
        else:
            return

def playerMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== Player Menu ===")
        retrieval_query("SELECT * FROM player")
        print("-------------------")
        print("1. Add a player")
        print("2. Modify a player")
        print("3. Delete a player")
        print("4. Back") 
        choice = int(input("Enter your choice: "))
        # Handle the user's choice
        if choice == 1:
            add_player()
        elif choice == 2:
            modify_player()
        elif choice == 3:
            delete_item("player")
        else:
            return

def rosterMenu():
    while True:
        os.system('clear') # Clear the screen
        retrieval_query("SELECT * FROM team")
        team_id = int(input("Select the ID of the team's rosters you want to view: "))
        print("=== Roster Menu ===")
        print("-------------------")
        print("1. Add a roster")
        print("2. Delete a roster")
        print("3. Back") 
        choice = int(input("Enter your choice: "))
        # Handle the user's choice
        if choice == 1:
            add_roster(team_id)
        elif choice == 2:
            delete_item("roster")
        else:
            return

def gameMenu():
    while True:
        os.system('clear') # Clear the screen
        retrieval_query("SELECT * FROM tournament")
        tournament_id = int(input("Select the ID of the tournament you want to display games of: "))
        print("=== Game Menu ===")
        retrieval_query("SELECT * FROM game WHERE tournament_id = " + str(tournament_id))
        print("-----------------")
        print("1. Add a game")
        print("2. Finish an incomplete game")
        print("3. Modify a game")
        print("4. Delete a game")
        print("5. Back") 
        choice = int(input("Enter your choice: "))
        # Handle the user's choice
        if choice == 1:
            add_game(tournament_id)
        if choice == 2:
            complete_game(tournament_id)
        elif choice == 3:
            modify_game(tournament_id)
        elif choice == 4:
            delete_item("game")
        else:
            return


## =========================== VIEW MENUS =========================== ##

def viewMenu():
    while True:
        os.system('clear') # Clear the screen
        print("=== View Menu ===")
        print("-----------------")
        print("1. List Tournaments")
        print("2. List Teams")
        print("3. List Players")
        print("4. Back") 
        choice = int(input("Enter your choice: "))
        os.system('clear') # Clear the screen
        # Handle the user's choice
        if choice == 1:
            listTournaments()
        elif choice == 2:
            listTeams()
        elif choice == 3:
            listPlayers()
        else:
            return

def listTournaments(filter_attr = "", filter_val = -1):
    no_quit = True
    while no_quit:
        if filter_attr == "team_id":
            query = ("SELECT T.tournament_id, tournament_name, start_day, start_month, start_year, street_address, city, state, result AS placement "
                    "FROM tournament T JOIN tournament_participant P ON T.tournament_id = P.tournament_id WHERE team_id = " + str(filter_val))
        else:
            query = "SELECT * FROM tournament"
        retrieval_query(query)

        tourney_id = int(input("Select torunament ID you want to view more information about (-1 to go back, -2 to quit to menu): "))
        if tourney_id == -1:
            return True
        elif tourney_id == -2:
            return False
        else:
            print("1. View participating teams")
            print("2. View games")
            print("3. Go back")
            choice = int(input("Select an option: "))

            if(choice == 1):
                no_quit = listTeams("tournament_id", tourney_id)
            elif(choice == 2):
                no_quit = listGames("tournament_id", tourney_id)
            else:
                print("Invalid choice")
                
def listGames(filter_attr = "", filter_val = -1):
    no_quit = True
    while no_quit:
        if filter_attr == "team_id":
            query = ("SELECT game_id, tournament_name, team_1_id, team_2_id, start_time, start_day, start_month, start_year, duration, winner_team_id "
                    "FROM game NATURAL JOIN tournament WHERE team_1_id = " + str(filter_val) + " OR team_2_id = " + str(filter_val) + ";"
            )
        elif filter_attr == "player_id":
            query = ("SELECT G.game_id, tournament_name, team_1_id, team_2_id, start_time, start_day, start_month, start_year, duration, winner_team_id, kills, deaths "
                    "FROM (SELECT * FROM game NATURAL JOIN tournament) G NATURAL JOIN game_participant P WHERE player_id =" + str(filter_val)) + ";"
        else:
            query = ("SELECT game_id, team_1_id, team_2_id, start_time, start_day, start_month, start_year, duration, winner_team_id "
                    "FROM game WHERE " + filter_attr + " = " + str(filter_val) + ";"
            )
        retrieval_query(query)

        game_id = int(input("Select game ID you want to view more information about (-1 to go back, -2 to quit to menu): "))
        if game_id == -1:
            return True
        elif game_id == -2:
            return False
        else:
            print("1. View participating teams")
            print("2. View participating players")
            print("3. Go back")
            choice = int(input("Select an option: "))
            if choice == 1:
                no_quit = listTeams("game_id", game_id)
            elif choice == 2:
                no_quit = listPlayers("game_id", game_id)
            else:
                print("Invalid choice")

def listTeams(filter_attr = "", filter_val = -1):
    no_quit = True
    while no_quit:
        if filter_attr == "tournament_id":
            query = ("SELECT T.team_id, team_name, win_rate, games_played, result AS placement "
            "FROM (SELECT * FROM team NATURAL JOIN team_win_rates) T NATURAL JOIN tournament_participant P WHERE tournament_id = " + str(filter_val)
            + " ORDER BY win_rate DESC;"
            )
        elif filter_attr == "game_id":
            query = ("SELECT T.team_id, team_name, win_rate, games_played, CASE WHEN team_id = winner_team_id THEN 'Winner' ELSE 'Loser' END AS game_result "
            "FROM (SELECT * FROM team NATURAL JOIN team_win_rates) T JOIN game G ON T.team_id = G.team_1_id OR T.team_id = G.team_2_id WHERE game_id = " + str(filter_val)
            + " ORDER BY win_rate DESC;"
            )
        elif filter_attr == "player_id":
            team_id = retrieve_attr_val("player", filter_val, "team_id")
            query = "SELECT team_id, team_name, win_rate, games_played FROM team NATURAL JOIN team_win_rates WHERE team_id =" + str(team_id) + " ORDER BY win_rate DESC;"
        else:
            query = "SELECT team_id, team_name, win_rate, games_played FROM team NATURAL JOIN team_win_rates ORDER BY win_rate DESC;"
        retrieval_query(query)

        team_id = int(input("Select team ID you want to view more information about (-1 to go back, -2 to quit to menu): "))
        if team_id == -1:
            return True
        elif team_id == -2:
            return False
        else:
            print("1. View past games")
            print("2. View team members")
            print("3. View past tournaments")
            print("4. Go back")
            choice = int(input("Select an option: "))

            if choice == 1:
                no_quit = listGames("team_id", team_id)
            elif choice == 2:
                no_quit = listPlayers("team_id", team_id)
            elif choice == 3:
                no_quit = listTournaments("team_id", team_id)
            else:
                print("Invalid choice")

def listPlayers(filter_attr = "", filter_val = -1):
    no_quit = True
    while no_quit:
        if filter_attr == "game_id":
            query = ("SELECT P.player_id, in_game_name, team_id, first_name, last_name, start_day, start_month, start_year, kills AS kills_this_game, deaths AS deaths_this_game "
            "FROM player P JOIN game_participant G ON G.player_id = P.player_id WHERE game_id = " + str(filter_val)
            + " ORDER BY kills DESC;"
            )
        elif filter_val != -1:
            query = "SELECT * FROM player NATURAL JOIN player_kill_death_ratio WHERE " + filter_attr + " = " + str(filter_val) + " ORDER BY kill_death_ratio DESC;"
        else:
            query = "SELECT * FROM player NATURAL JOIN player_kill_death_ratio ORDER BY kill_death_ratio DESC;"
        retrieval_query(query)

        player_id = int(input("Select player ID you want to view more information about (-1 to go back, -2 to quit to menu): "))
        if player_id == -1:
            return True
        elif player_id == -2:
            return False
        else:
            print("1. View past games")
            print("2. View team")
            print("3. Go back")
            choice = int(input("Select an option: "))

            if choice == 1:
                no_quit = listGames("player_id", player_id)
            elif choice == 2:
                no_quit = listTeams("player_id", player_id)
            else:
                print("Invalid choice")

# Create an infinite loop to show the menu and handle user input
while True:
  mainMenu()
  choice = int(input("Enter your choice: "))
  if choice == 1:
    print("Not yet implemented.")
    editMenu() # List all tables
  elif choice == 2:
    print("Not yet implemented.")
    viewMenu() # Describe a table
  elif choice == 3:
    debug() # Execute a query
  elif choice == 4:
    break
  else:
    print("Invalid choice")
