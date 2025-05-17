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
                return redirect(url_for("index"))
            
            #updates homepage.html with error message
            return render_template("homepage.html",error= error_message)
        

    return render_template("homepage.html")

#used to add a new user to the database
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        pass

#will load the users info onto this page
@app.route("/index", methods = ["GET","POST"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)