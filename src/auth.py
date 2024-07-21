from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests

load_dotenv()
MgPass = os.getenv('MongoPass')
MgUser = os.getenv('MongoUser')

uri = 'mongodb+srv://'+MgUser+':'+ MgPass +'@cluster0.uexvwf7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key
client = MongoClient(uri,27017)
db = client['GuessTheVerb']  # Replace with your MongoDB database name
users_collection = db['users']

@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def guess_the_verb():
    # if "username" in session:
    #     user = session["username"]
    #     return 'Welcome to GuessTheVerb'
    # else:
    #     return redirect(url_for("login"))
    msg = ''
    return render_template('login.html', msg='')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': password,'email':email})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg =''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['loggedin'] = True
            session['username'] = user['username']
            msg = 'Login successful!'
            return redirect(url_for('game'))
            
        else:
            msg = 'Invalid username or password. Please try again.'

    return render_template('login.html', msg=msg)


@app.route('/game', methods=['GET', 'POST'])
def game():
    msg = 'Welcome!'
    if session['loggedin'] == True:
        print(session['loggedin'])
        guesses = []
    
        if request.method == 'POST':
            guess = request.form['guess']
            ### ADD Lilyan's Game Logic ###
            ### ADD  Bao's Scorning Logic ###
            msg = 'Your guess was: '+guess
            guesses.append(guess)

            uri = 'http://127.0.0.1:8000/'+guess
            gamelogic = requests.get(uri)
            score = gamelogic.json().get("score")
            chosen_word = gamelogic.json().get("chosen_word")
            msg = 'Your guess was: '+ chosen_word + ' and score: '+ str(score)

            return render_template('game.html', len=len(guesses), guesses=guesses, msg=msg)

       
    else:
        guesses.clear()
        return render_template('login.html', msg="Please Login")

    return render_template('game.html',msg=msg)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    return redirect(url_for('login'))

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()

    #https://www.geeksforgeeks.org/build-your-own-microservices-in-flask/