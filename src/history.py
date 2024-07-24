from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GuessHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    guess = db.Column(db.String(50), nullable=False)

def add_guess(user_id, guess):
    new_guess = GuessHistory(user_id=user_id, guess=guess)
    db.session.add(new_guess)
    db.session.commit()

def get_history(user_id):
    return GuessHistory.query.filter_by(user_id=user_id).all()
