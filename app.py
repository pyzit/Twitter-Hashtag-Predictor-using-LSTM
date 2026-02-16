from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

app = Flask(__name__)

# 1️⃣ Load your trained model, tokenizer, and mlb
model_lstm = load_model('model_lstm.h5')

with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open('mlb.pkl', 'rb') as f:
    mlb = pickle.load(f)

max_len = 100  # same as used during training

# 2️⃣ Prediction function (Top K hashtags)
def predict_hashtags_top_k(new_text, top_k=3):
    seq = tokenizer.texts_to_sequences([new_text])
    padded = pad_sequences(seq, maxlen=max_len)
    probs = model_lstm.predict(padded)[0]
    top_indices = np.argsort(probs)[-top_k:][::-1]
    predicted_hashtags = [mlb.classes_[i] for i in top_indices]
    return predicted_hashtags

# 3️⃣ Flask routes
@app.route("/", methods=["GET", "POST"])
def home():
    hashtags = []
    tweet_text = ""
    if request.method == "POST":
        tweet_text = request.form["tweet"]
        hashtags = predict_hashtags_top_k(tweet_text)
    return render_template("index.html", tweet=tweet_text, hashtags=hashtags)

if __name__ == "__main__":
    app.run(debug=True)
