from pathlib import Path
import pickle

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "model_lstm.h5"
TOKENIZER_PATH = ARTIFACTS_DIR / "tokenizer.pkl"
MLB_PATH = ARTIFACTS_DIR / "mlb.pkl"

max_len = 100

model_lstm = load_model(MODEL_PATH)

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

with open(MLB_PATH, "rb") as f:
    mlb = pickle.load(f)


def predict_hashtags_top_k(new_text, top_k=3):
    seq = tokenizer.texts_to_sequences([new_text])
    padded = pad_sequences(seq, maxlen=max_len)
    probs = model_lstm.predict(padded)[0]
    top_indices = np.argsort(probs)[-top_k:][::-1]
    predicted_hashtags = [mlb.classes_[i] for i in top_indices]
    return predicted_hashtags
