from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import datetime as dt
import bson


load_dotenv()
MgPass = os.getenv('MongoPass')
MgUser = os.getenv('MongoUser')
 
uri = "mongodb+srv://allusers:rNjlBpOnKQReyiF8@cluster0.zbjwcra.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key
client = MongoClient(uri)#,27017)
db = client['GuessTheVerb']  # Replace with your MongoDB database name
users_collection = db['users']
sessionscore_collection = db['sescore']

@app.route('/')
def guess_the_verb():
    print("Accessing the home page")
    msg = ''
    session.clear()
    return render_template('login.html', msg=msg)


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
            time = dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            users_collection.insert_one({'username': username, 'password': password,'email':email, 'datecreated':time})
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
        print(session["username"])
    
        if request.method == 'POST':
            guess = request.form['guess']

            uri = 'http://127.0.0.1:8000/'+guess
            gamelogic = requests.get(uri)
            score = gamelogic.json().get("score")
            chosen_word = gamelogic.json().get("chosen_word")
            msg = 'Your guess was: '+ guess + ' and score: '+ str(score)

            user = {"username":session["username"]}


            if sessionscore_collection.find_one(user):
                sescores = sessionscore_collection.find_one(user) 
                sessionscore_collection.update_one(user, {'$push': {'scores': score,'guess':guess}})
                sessionscore_collection.update_one(user, {'$set': {'tries': sescores["tries"]+1}})
                sescores = sessionscore_collection.find_one(user) 
                
            else:
                sessionscore_collection.insert_one({"username":session["username"],'tries':1,'scores': [score],'guess':[guess]})
                sescores = sessionscore_collection.find_one(user)   
                 
            return render_template('game.html', guesses=sescores['guess'], scores=sescores['scores'], len=len(sescores['guess']))

    else:
        return render_template('login.html', msg="Please Login")

    return render_template('game.html',msg = 'Welcome!')

@app.route('/api/userdata')
def userdata():
    user = users_collection.find_one({'username': session["username"]})
    return jsonify({"usersession":session["tries"],"score": user["score"],"chosen_word":["chosen_word"]}) #jsonify({"guess":guess})


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    print(session)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    user = users_collection.find_one({'username': session["username"]})
    return render_template('profile.html',user=user["username"],email=user["email"], joined =user["datecreated"])


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug = True, port = 5001)

    #https://www.geeksforgeeks.org/build-your-own-microservices-in-flask/