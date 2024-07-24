import random
import Levenshtein
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

verbs = [
    "jump", "run", "eat", "sleep", "laugh", "cry", "sing", "dance", "swim", 
    "write", "read", "think", "talk", "listen", "cook", "play", "work", 
    "study", "draw", "paint", "climb", "drive", "fly", "fight", "travel", 
    "build", "clean", "wash", "fix", "cut", "grow", "plant", "push", 
    "pull", "throw", "catch", "kick", "punch", "shoot", "stab", 
    "save", "spend", "earn", "sell", "buy", "teach", "learn", "program"
]

def choose_word():
    return random.choice(verbs)

def calculate_score(guess, word): 
    distance = Levenshtein.distance(guess, word)
    max_distance = max(len(guess), len(word))
    score = max(100, (max_distance - distance) / max_distance * 1000)
    return score

# Lilyan's original code
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         user_guess = request.form['guess'].strip().lower()
#         chosen_word = request.form.get('chosen_word', choose_word())  # Default to a new word if not set
        
#         if user_guess == "give up":
#             return render_template('index.html', chosen_word=chosen_word, msg=f"You gave up! The correct word was: {chosen_word}")
            
#         elif user_guess == chosen_word:
#             score = 1000
#             return render_template('index.html', chosen_word=chosen_word, msg="Congratulations! You guessed it right!", score=score)
#         else:
#             score = calculate_score(user_guess, chosen_word)
#             return render_template('index.html', chosen_word=chosen_word, msg=f"Score: {score:.2f}/1000")
    
#     # Initial page load
#     chosen_word = choose_word()
#     return render_template('index.html', chosen_word=chosen_word)

## Bhushan's update:

@app.route('/<guess>', methods=['GET'])
def gamelogic(guess):
    user_guess = guess.strip().lower()
    chosen_word = choose_word()  # Default to a new word if not set
    score = calculate_score(user_guess, chosen_word)
    print(guess)
    print(chosen_word)
    return  jsonify({"score": score,"chosen_word":chosen_word}) #jsonify({"guess":guess})

if __name__ == '__main__':
    app.run(port=8000)
import random
import Levenshtein
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# English verbs
english_verbs = [
    "jump", "run", "eat", "sleep", "laugh", "cry", "sing", "dance", "swim", 
    "write", "read", "think", "talk", "listen", "cook", "play", "work", 
    "study", "draw", "paint", "climb", "drive", "fly", "fight", "travel", 
    "build", "clean", "wash", "fix", "cut", "grow", "plant", "push", 
    "pull", "throw", "catch", "kick", "punch", "shoot", "stab", 
    "save", "spend", "earn", "sell", "buy", "teach", "learn", "program"
]

# Spanish verbs
spanish_verbs = [
    "saltar", "correr", "comer", "dormir", "reír", "llorar", "cantar", "bailar", "nadar", 
    "escribir", "leer", "pensar", "hablar", "escuchar", "cocinar", "jugar", "trabajar", 
    "estudiar", "dibujar", "pintar", "escalar", "conducir", "volar", "pelear", "viajar", 
    "construir", "limpiar", "lavar", "arreglar", "cortar", "cultivar", "plantar", "empujar", 
    "tirar", "agarrar", "patear", "golpear", "disparar", "apuñalar", 
    "ahorrar", "gastar", "ganar", "vender", "comprar", "enseñar", "aprender", "programar"
]

#New Code
'''def choose_word(language='english'):
    if language == 'spanish':
        return random.choice(spanish_verbs)
    else:
        return random.choice(english_verbs)

def calculate_score(guess, word): 
    distance = Levenshtein.distance(guess, word)
    max_distance = max(len(guess), len(word))
    score = max(100, (max_distance - distance) / max_distance * 1000)
    return score

@app.route('/<language>/<guess>', methods=['GET'])
def gamelogic(language, guess):
    user_guess = guess.strip().lower()
    chosen_word = choose_word(language)
    score = calculate_score(user_guess, chosen_word)
    print(f"User guess: {user_guess}")
    print(f"Chosen word: {chosen_word}")
    return jsonify({"score": score, "chosen_word": chosen_word})

@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form.get('language', 'english')
    # Store the selected language in the session or other mechanism
    session['language'] = language
    return jsonify({"message": "Language set", "language": language})

if __name__ == '__main__':
    app.run(port=8000)'''
