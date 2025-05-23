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

                print("Form keys received:", list(request.form.keys()))
                print("username:", request.form.get("username"))
                print("password:", request.form.get("password"))

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

    if user_data is None:
        return "User not found", 404

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

    con.close()

    #loops through each row
    for stats in table_stats:
        new_dict = {"event": stats[0], "team": stats[1], "date": stats[2], "location": stats[3]}
        data.append(new_dict)

    return render_template("index.html",name = first_name, data = data, username = username)


@app.route("/about/<username>", methods = ["GET","POST"])
def about(username):

    #retrieves user info
    con = sqlite3.connect('intramural.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM User WHERE username = ?',(username,))
    info = cur.fetchone()


    user = {'name' : info[1]+' '+info[2],'username': info[4], 'password':info[3], 'email':info[5], 'role':info[6]}

    if user['role'] == 'A':
        user['role'] = 'Admin'
    else:
        user['role'] = 'User'
    

    #updates user info
    if request.method == 'POST':

        signed = request.form.get("sign")
        if signed:
            first_name = request.form.get('fname')
            last_name = request.form.get('lname')
            password = request.form.get('pass')
            mail = request.form.get('mail')

            if first_name:
                cur.execute('UPDATE User SET first_name = ? WHERE username = ?',(first_name,username))
                con.commit()
            
            if last_name:
                cur.execute('UPDATE User SET last_name = ? WHERE username = ?',(last_name,username))
                con.commit()
            
            if password:
                cur.execute('UPDATE User SET password = ? WHERE username = ?',(password,username))
                con.commit()

            if mail:
                cur.execute('UPDATE User SET mail = ? WHERE username = ?',(mail,username))
                con.commit()

            con.close()
            return redirect(url_for('about', username=username))
            

    return  render_template("about.html",username=username, user=user)



@app.route("/events/<username>",methods=["POST","GET"])
def events(username):
    #displays information for user

    #display current events
    current_events = []

    con = sqlite3.connect('intramural.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM User WHERE username = ?',(username,))
    info = cur.fetchone()

    user_id = info[0]

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
    
    table_stats = table_info.fetchall()

    for stats in table_stats:
        new_dict = {"event": stats[0], "team": stats[1], "date": stats[2], "location": stats[3]}
        current_events.append(new_dict)


    #display joinabale events
    joinable_events = []
    joinable_info = cur.execute('''SELECT 
                                SE.event_id,
                                SE.event_name, 
                                SE.date, 
                                SE.location
                                FROM SportEvent SE
                                WHERE NOT EXISTS (
                                    SELECT 1
                                    FROM Team T
                                    JOIN UserToTeam UT ON UT.team_id = T.team_id
                                    WHERE T.event_id = SE.event_id AND UT.user_id = ?
                                )
                                ORDER BY SE.date DESC;''',(user_id,))
    
    joinable_stats = joinable_info.fetchall()
    for stats in joinable_stats:
        new_dict = {"id": stats[0], "name": stats[1], "date": stats[2], "location": stats[3]}
        joinable_events.append(new_dict)

    return render_template("events.html", username=username, current_events = current_events, joinable_events = joinable_events)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)