import sqlite3
import csv


con = sqlite3.connect('intramural.db')
cur = con.cursor()

#remove table during multiple runs
cur.execute('DROP TABLE IF EXISTS User;')
cur.execute('DROP TABLE IF EXISTS Team;')
cur.execute('DROP TABLE IF EXISTS SportEvent;')
cur.execute('DROP TABLE IF EXISTS userToTeam;')

#create users table
create_table = '''CREATE TABLE User(user_id INTEGER PRIMARY KEY AUTOINCREMENT,first_name TEXT,last_name TEXT,password TEXT,username TEXT,email TEXT,role TEXT);'''
cur.execute(create_table)

#inserts records into User
file = open('User.csv')
contents = csv.reader(file)
header = next(contents)
insert_records = '''INSERT INTO User(user_id, first_name, last_name, password, username, email, role) VALUES (?, ?, ?, ?, ?, ?, ?)'''
cur.executemany(insert_records, contents)
con.commit()
file.close()

#create Teams table
create_table = '''CREATE TABLE Team(team_id INTEGER PRIMARY KEY AUTOINCREMENT,team_name TEXT,user_id INTEGER, event_id INTEGER);'''
cur.execute(create_table)

#insert records into User
file = open('Team.csv')
contents = csv.reader(file)
header = next(contents)
insert_record = '''INSERT INTO Team(team_id, team_name, user_id, event_id) VALUES (?,?,?,?)'''
cur.executemany(insert_record, contents)
con.commit()
file.close()

#create SportEvent table
create_table = '''CREATE TABLE SportEvent(event_id INTEGER PRIMARY KEY AUTOINCREMENT, event_name TEXT, date TEXT, location TEXT, admin_id INTEGER);'''
cur.execute(create_table)

#insert records into SportEvent
file = open('Sport_Event.csv')
contents = csv.reader(file)
header = next(contents)
insert_record = '''INSERT INTO SportEvent(event_id, event_name, date, location, admin_id) VALUES (?, ?, ?, ?, ?)'''
cur.executemany(insert_record, contents)
con.commit()
file.close()

#create UserToTeam table
create_table = '''CREATE TABLE UserToTeam(user_id INTEGER,team_id INTEGER);'''
cur.execute(create_table)

#insert records into UserToTeam
file = open('User_to_team.csv')
contents = csv.reader(file)
header = next(contents)
insert_record = '''INSERT INTO UserToTeam(user_id, team_id) VALUES (?,?)'''
cur.executemany(insert_record, contents)
con.commit()
file.close()