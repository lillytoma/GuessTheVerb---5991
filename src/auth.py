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
client = MongoClient(uri)
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
            users_collection.insert_one({'username': username, 'password': password, 'email': email, 'datecreated': time, 'score': 0})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
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
    if session['loggedin']:
        print(session['loggedin'])
        print(session["username"])

        user_record = users_collection.find_one({"username": session["username"]})
        user_score = user_record.get('score', 0)  # Default to 0 if score is missing

        if request.method == 'POST':
            user = {"username": session["username"]}

            if 'giveup' in request.form:
                sessionscore_collection.delete_one(user)
                session.pop('chosen_word', None)  # Clear chosen word from session
                msg = 'Start Over!'
            else:
                guess = request.form['guess']
                language = request.form.get('language', 'english')  # Default to English if not specified

                if 'chosen_word' not in session:
                    chosen_word = requests.get(f'http://127.0.0.1:8000/choose_word/{language}').json().get('chosen_word')
                    session['chosen_word'] = chosen_word
                else:
                    chosen_word = session['chosen_word']

                uri = f'http://127.0.0.1:8000/{guess}/{chosen_word}/{language}'
                gamelogic = requests.get(uri)
                score = gamelogic.json().get("score")

                if score == 1000:
                    sessionscore_collection.delete_one(user)
                    session.pop('chosen_word', None)  # Clear chosen word from session
                    users_collection.update_one({"username": session["username"]}, {'$inc': {'score': 100}})
                    user_score += 100  # Update local variable
                    msg = 'You Won! Start Over'
                else:
                    if sessionscore_collection.find_one(user):
                        sescores = sessionscore_collection.find_one(user)
                        sessionscore_collection.update_one(user, {'$push': {'scores': score, 'guess': guess}})
                        sessionscore_collection.update_one(user, {'$set': {'tries': sescores["tries"] + 1}})
                        sescores = sessionscore_collection.find_one(user)
                        users_collection.update_one({"username": session["username"]}, {'$inc': {'score': -10}})
                        user_score -= 10  # Update local variable
                        guesses = sescores['guess']
                        scores = sescores['scores']
                        msg = f'Your guess was: {guesses[-1]} and similarity score: {scores[-1]}'
                    else:
                        sessionscore_collection.insert_one({"username": session["username"], 'tries': 1, "word": chosen_word, 'scores': [score], 'guess': [guess]})
                        sescores = sessionscore_collection.find_one(user)
                        guesses = sescores['guess']
                        scores = sescores['scores']
                        msg = f'Your guess was: {guesses[-1]} and similarity score: {scores[-1]}'

                    return render_template('game.html', guesses=guesses, scores=scores, len=len(guesses), user_score=user_score, msg=msg)

        return render_template('game.html', user_score=user_score, msg=msg)

    return render_template('login.html', msg="Please Login")


@app.route('/api/rankings')
def rankings():
    top_users = users_collection.find().sort("score", -1).limit(10)
    ranking_list = []
    for index, user in enumerate(top_users, start=1):
        score = user.get('score', 0)  # Use 0 if score is missing
        ranking_list.append({"rank": index, "username": user['username'], "score": score})
    return jsonify(ranking_list)


@app.route('/api/userdata')
def userdata():
    user = users_collection.find_one({'username': session["username"]})
    return jsonify({"usersession": session.get("tries", 0), "score": user.get("score", 0), "chosen_word": session.get("chosen_word", "")})


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    print(session)
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    user_record = users_collection.find_one({'username': session["username"]})
    user_score = user_record.get('score', 0)
    
    # Calculate user ranking
    all_users = users_collection.find().sort("score", -1)
    ranking = 1
    for user in all_users:
        if user['username'] == session["username"]:
            break
        ranking += 1
    
    return render_template('profile.html', user=user_record["username"], email=user_record["email"], joined=user_record["datecreated"], score=user_score, ranking=ranking)


# main driver function
if __name__ == '__main__':
    app.run(debug=True, port=5001)
