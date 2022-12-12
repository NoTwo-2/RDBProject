# DBProject
School database project
Project members: Jacob, Hari, Nathan

# Includes
- ER Diagram and Relational Schema (.drawio)
- Android app inventor project file (.aia)
- Mysql dump file (.sql)
- Python CLI implementation (.py)

# Installation Instructions

## Server setup
If you do not already have a MySQL server, this is how to set one up.
1. Install mysql if you have not already
2. Complete the server setup guide. Set username to "root" and remember the password you use

## Database setup
1. Run MySQL workbench and connect to the server you just set up
2. In the navigator window, select "Data Import/Restore"
3. Select "Import from Self-Contained File," specify the location of esports.sql
4. Click "Start Import"

## Python Setup
1. In this directory, create a new python script file called “secret.py”
2. Insert the following code into secret.py and replace your_password with the password you used to create the MySQL server. Save and close after you’re finished. 
    
        password = "your_password"
3. Change directories into the python scripts directory. It should be in this location:
        
        C:\Users\user_name\AppData\Local\Programs\Python\Python311\Scripts
4. Run the following commands:

        pip3 install mysql-connector-python
	    pip3 install tabular
You are now ready to run the python script!

        python3 mysqlProject.py 