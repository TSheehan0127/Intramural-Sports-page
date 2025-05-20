from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import json
import sqlite3
from sqlite3 import IntegrityError



app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def homepage():
    if request.method == "POST":
        print("page loaded")
        error_message = " "
        action = request.form.get("action")

        #checks which button was pressed
        if action == "signup":
            print("signup button pressed")
            return redirect(url_for("signup"))
        elif action == "login":
            user = request.form.get("username")
            password = request.form.get("password")

            #checks for login validation
            con = sqlite3.connect('intramural.db')
            cur = con.cursor()
            
            cur.execute('SELECT * FROM User WHERE username = ? AND password = ?',(user, password))
            valid = cur.fetchone()

            if valid is None:
                error_message = "Invalid username or password"
                print("login unsuccessful")
                
            else:
                #switches to index.html
                print("login successful!")
                return redirect(url_for("index", username=user))
            
            #updates homepage.html with error message
            return render_template("homepage.html",error= error_message)
        

    return render_template("homepage.html")

#used to add a new user to the database
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        signed = request.form.get("sign")
        if signed:

            user_name = request.form.get("userN")

            #username / pass validation
            con = sqlite3.connect('intramural.db')
            cur= con.cursor()

            cur.execute('SELECT * FROM User WHERE username = ?',(user_name,))
            valid = cur.fetchone()

            if valid is not None:
                #displays error message
                error_message = "username already taken or is invalid"
                return render_template('signup.html', error= error_message)
            
            #adds user to database
            first_name= request.form.get("fname")
            last_name= request.form.get("lname")
            password = request.form.get("pass")
            email = request.form.get("mail")
            insert_record = "INSERT INTO User(first_name, last_name, password, username, email, role) VALUES (?, ?, ?, ?, ?, ?)"

            cur.execute(insert_record, (first_name, last_name, password, user_name, email, 'U'))
            con.commit()
            con.close()

            #TODO add message on homepage.html, that notifies user they have been added
            print("successfuly added user!")
            return redirect(url_for("homepage"))
        
    return render_template('signup.html')

#will load the users info onto this page
@app.route("/index/<username>", methods = ["GET","POST"])
def index(username):

    #retrieves user data:
    con = sqlite3.connect('intramural.db')
    cur=con.cursor()
    cur.execute('SELECT * FROM User WHERE username = ?',(username,))
    user_data = cur.fetchone()
    user_id = user_data[0]
    first_name = user_data[1]
    last_name = user_data[2]
    password = user_data[3]
    email = user_data[5]
    role = user_data[6]
    
    # retrieves user information and displays it on index table
    data = []

    #selects event, team, date, and location for index page.
    table_info = cur.execute('''SELECT 
                             SportEvent.event_name, 
                             Team.team_name, 
                             SportEvent.date, 
                             SportEvent.location, 
                             UserToTeam.user_id 
                             FROM SportEvent 
                             JOIN Team ON Team.event_id = SportEvent.event_id 
                             JOIN UserToTeam ON UserToTeam.team_id = Team.team_id 
                             WHERE UserToTeam.user_id = ?
                             ORDER BY date desc;''',(user_id,))
    
    table_stats = table_info.fetchall();

    #loops through each row
    for stats in table_stats:
        new_dict = {"event": stats[0], "team": stats[1], "date": stats[2], "location": stats[3]}
        data.append(new_dict)

    return render_template("index.html",name = first_name, data = data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)