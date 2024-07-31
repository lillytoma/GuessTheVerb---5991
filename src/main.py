import random
import Levenshtein
from flask import Flask, jsonify

app = Flask(__name__)

english_verbs = [
    "jump", "run", "eat", "sleep", "laugh", "cry", "sing", "dance", "swim",
    "write", "read", "think", "talk", "listen", "cook", "play", "work",
    "study", "draw", "paint", "climb", "drive", "fly", "fight", "travel",
    "build", "clean", "wash", "fix", "cut", "grow", "plant", "push",
    "pull", "throw", "catch", "kick", "punch", "shoot", "stab",
    "save", "spend", "earn", "sell", "buy", "teach", "learn", "program"
]

spanish_verbs = [
    "saltar", "correr", "comer", "dormir", "reír", "llorar", "cantar", "bailar", "nadar",
    "escribir", "leer", "pensar", "hablar", "escuchar", "cocinar", "jugar", "trabajar",
    "estudiar", "dibujar", "pintar", "escalar", "conducir", "volar", "pelear", "viajar",
    "construir", "limpiar", "lavar", "arreglar", "cortar", "cultivar", "plantar", "empujar",
    "tirar", "agarrar", "patear", "golpear", "disparar", "apuñalar",
    "ahorrar", "gastar", "ganar", "vender", "comprar", "enseñar", "aprender", "programar"
]

def choose_word(language):
    if language == 'spanish':
        return random.choice(spanish_verbs)
    return random.choice(english_verbs)

def calculate_score(guess, word):
    distance = Levenshtein.distance(guess, word)
    max_distance = max(len(guess), len(word))
    score = max(100, (max_distance - distance) / max_distance * 1000)
    return score

@app.route('/choose_word/<language>', methods=['GET'])
def choose_word_endpoint(language):
    chosen_word = choose_word(language)
    return jsonify({"chosen_word": chosen_word})

@app.route('/<guess>/<word>/<language>', methods=['GET'])
def gamelogic(guess, word, language):
    user_guess = guess.strip().lower()
    if word == "first":
        chosen_word = choose_word(language)
    else:
        chosen_word = word
    score = calculate_score(user_guess, chosen_word)
    print(guess)
    print(word)
    return jsonify({"score": score, "chosen_word": chosen_word})

if __name__ == '__main__':
    app.run(port=8000)
