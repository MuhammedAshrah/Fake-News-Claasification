from flask import Flask, render_template, request
from flask_cors import CORS
from tensorflow.keras.models import load_model
import pickle
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(8), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'{{"id": "{self.id}", "article": "{self.article}", "result": "{self.result}", "confidence": "{self.confidence}"}}'

model = load_model('models/model.h5')

with open('models/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

def preprocess_text(article, tokenizer):
    sequence = tokenizer.texts_to_sequences([article])
    padded_sequence = pad_sequences(sequence, maxlen=200)
    return padded_sequence

@app.route('/')
def home():
    # db.drop_all()
    db.create_all()
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_article():
    article = request.form['article']
    padded = preprocess_text(article, tokenizer)

    # Get raw prediction
    raw_prediction = model.predict(padded)[0][0]

    # Determine result and confidence
    if raw_prediction >= 0.5:
        result = "Real"
        confidence = raw_prediction * 100
    else:
        result = "Fake"
        confidence = (1 - raw_prediction) * 100

    log = Log(article=article, result=result, confidence=confidence)
    db.session.add(log)
    db.session.commit()
    return render_template('index.html', result=result, confidence=f"{confidence:.2f}%")

@app.route('/log')
def log():
    logs = Log.query.all()
    return render_template('log.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
