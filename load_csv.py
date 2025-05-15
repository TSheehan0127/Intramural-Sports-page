import sqlite3
import csv


con = sqlite3.connect('intramural.db')
cur = con.cursor()

#remove table during multiple runs
cur.execute('DROP TABLE IF EXISTS User;')

#create users table
create_table = '''CREATE TABLE User('user_id','first_name','last_name','password','username','email','role');'''
cur.execute(create_table)


