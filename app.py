from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import pickle
import numpy as np# Load trained model

from tensorflow.keras.preprocessing.sequence import pad_sequences

# Initialize Flask app
app = Flask(__name__)

model = load_model('models/model.h5')

# Load tokenizer
with open('models/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

def preprocess_text(article, tokenizer):
    sequence = tokenizer.texts_to_sequences([article])
    padded_sequence = pad_sequences(sequence, maxlen=200)
    return padded_sequence

@app.route('/')
def home():
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

    return render_template('index.html', result=result, confidence=f"{confidence:.2f}%")

if __name__ == '__main__':
    app.run(debug=True)
