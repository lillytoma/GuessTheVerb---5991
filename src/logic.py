from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import Levenshtein

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0)
    consecutive_correct_guesses = db.Column(db.Integer, default=0)

# Example target word (in a real application, this would be dynamic)
target_word = "example"

@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    user_id = data['user_id']
    guess = data['guess']
    correct = guess == target_word

    score_entry = Score.query.filter_by(user_id=user_id).first()
    if not score_entry:
        score_entry = Score(user_id=user_id)
        db.session.add(score_entry)

    if correct:
        score_entry.score += 10
        score_entry.consecutive_correct_guesses += 1
        if score_entry.consecutive_correct_guesses % 3 == 0:
            score_entry.score += 5
    else:
        score_entry.score -= 1
        score_entry.consecutive_correct_guesses = 0

    db.session.commit()

    # Calculate similarity score
    similarity_score = Levenshtein.ratio(guess, target_word)

    return jsonify({'user_id': user_id, 'score': score_entry.score, 'similarity': similarity_score})

@app.route('/get_rankings', methods=['GET'])
def get_rankings():
    rankings = Score.query.order_by(Score.score.desc()).all()
    return jsonify([{'user_id': s.user_id, 'score': s.score} for s in rankings])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
