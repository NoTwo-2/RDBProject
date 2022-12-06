import mysql.connector

# host      = localhost if the demo is running the MySQL DB on the local machine 
# otherwise, we will figure it out when the time comes
# user      = username (duh) 
# password  = try to set up a secret file. we dont want our password pushed up into our git repo
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword"
)

# TODO: add functions from the google doc

# https://www.w3schools.com/python/python_mysql_getstarted.asp