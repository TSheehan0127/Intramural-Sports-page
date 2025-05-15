from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import json
import sqlite3
from sqlite3 import IntegrityError


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("homepage.html")




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)