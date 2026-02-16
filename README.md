## Twitter Hashtag Predictor using LSTM

Improved and maintained by @pyzit.

Intelligent suggestion engine that predicts relevant hashtags for a tweet using a pre-trained LSTM (Long Short-Term Memory) neural network. The project is designed for:

- local development with a simple Flask web UI
- clear, modular architecture suitable for open-source contributions
- easy extension to APIs, dashboards, and production deployment

---

## Features

- Predicts top-k hashtags for a given tweet
- Simple web interface built with Flask
- Modular package structure:
  - prediction pipeline isolated in a dedicated module
  - HTTP routes separated from core ML logic
  - templates organized under a standard `templates/` directory
- Ready to be wrapped as an API (REST) or integrated into other services

---

## Tech Stack

- **Language:** Python 3.9+
- **Web Framework:** Flask
- **Deep Learning:** TensorFlow / Keras
- **Data Science:** NumPy, pandas, scikit-learn
- **Model:** LSTM-based neural network for multi-label hashtag prediction

---

## Project Structure

Current high-level layout:

```text
.
├── app.py                      # Flask entrypoint (uses application factory)
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project metadata (optional tooling)
├── artifacts/
│   ├── model_lstm.h5           # Pre-trained LSTM model (binary artifact)
│   ├── tokenizer.pkl           # Trained tokenizer for tweets
│   └── mlb.pkl                 # MultiLabelBinarizer for hashtag encoding
├── hashtag_predictor/
│   ├── __init__.py             # create_app factory, blueprint registration
│   ├── prediction.py           # model loading & prediction utilities
│   ├── routes.py               # Flask routes / view functions
│   └── templates/
│       └── index.html          # Web UI template
└── README.md                   # You are here
```

---

## Core Use Case

**Goal:** Given a tweet (raw text), suggest the most relevant hashtags the user should add.

Common scenarios:

- drafting social media posts and automatically discovering trending / relevant tags
- helping marketing teams keep hashtag usage consistent across campaigns
- running experiments on hashtag performance by logging predictions vs. actual engagement

---

## Requirements

### Python and OS

- Python **3.9.25 or higher** (3.9.x series recommended)
- Windows, macOS or Linux (project is OS-agnostic)

### Python dependencies

Listed in `requirements.txt`:

- Flask
- tensorflow
- numpy
- scikit-learn
- pandas
- pickle5

You can manage them via `pip` or pin them in `pyproject.toml` / your preferred tool.

---

## Quick Start (Local Development)

From the project root:

```bash
cd Twitter-Hashtag-Predictor-using-LSTM
python -m venv .venv
source .venv/bin/activate           # macOS / Linux
# or
.venv\Scripts\Activate.ps1          # Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```

Run the Flask app:

```bash
python app.py
```

Open in your browser:

- http://127.0.0.1:5000
  or
- http://localhost:5000

You should see a simple page where you can paste a tweet and receive suggested hashtags.

---

## Application Architecture

High-level architecture (runtime):

```text
Browser (user)
    │
    ▼
Flask app (app.py -> create_app)
    │
    ├── Blueprint: main (routes.py)
    │       └─ "/" [GET, POST]
    │
    └── Prediction service (prediction.py)
            ├─ tokenizer.pkl
            ├─ model_lstm.h5
            └─ mlb.pkl
```

### Application factory (`create_app`)

Located in `hashtag_predictor/__init__.py`:

- creates a Flask application instance
- registers the main blueprint
- sets template folder location (`templates`)

This pattern is compatible with:

- unit tests that need isolated app instances
- WSGI servers (gunicorn, uWSGI, etc.)

### Routing

`hashtag_predictor/routes.py` defines:

- `"/"` route that:
  - on **GET**: renders the form with an empty tweet
  - on **POST**: reads user input, calls the prediction function, and re-renders with suggested hashtags

---

## Prediction Pipeline (Logic)

The core prediction logic lives in `hashtag_predictor/prediction.py`.

Conceptual steps when a tweet comes in:

1. **Text preprocessing**
   - the raw tweet string is passed to a Keras `Tokenizer` (loaded from `tokenizer.pkl`)
   - text is converted into a sequence of integer token IDs
2. **Sequence padding**
   - sequences are padded/truncated to a fixed `max_len` (e.g. 100 tokens)
3. **Model inference**
   - the padded sequence is fed into the LSTM model (`model_lstm.h5`)
   - the model outputs a probability for each possible hashtag class
4. **Top-K selection**
   - the probabilities are sorted
   - the top `k` indices are selected (default: `k = 3`)
   - those indices are mapped back to hashtag strings via `mlb.classes_`
5. **Return hashtags**
   - the function returns a list of predicted hashtags as strings

This is a **multi-label classification** setup where each tweet can have multiple correct hashtags.

---

## Web UI Flow

**Template:** `hashtag_predictor/templates/index.html`

- Single form with:
  - text input (`name="tweet"`)
  - submit button (`Predict`)
- On submit:
  - the browser sends a POST request to `/`
  - server computes predictions and re-renders the same template with:
    - original tweet shown in the input
    - list of suggested hashtags below

This UX makes it very easy to experiment iteratively with different tweets.

---

## Data & Training (Conceptual)

The repository includes **trained artifacts**:

- `model_lstm.h5`
- `tokenizer.pkl`
- `mlb.pkl`

The training pipeline itself is **not** included in this repository. However, a typical training flow for this project looks like:

1. **Collect data**
   - tweets with associated hashtags (e.g. from Twitter API, Kaggle datasets, etc.)
2. **Preprocess**
   - clean text (lowercase, remove URLs, mentions, emojis as needed)
   - filter or normalize hashtags (e.g. remove `#` prefix, deduplicate)
3. **Encode**
   - fit a `Tokenizer` on tweet texts
   - transform each tweet into integer sequences
   - use `MultiLabelBinarizer` to encode hashtags into multi-hot vectors
4. **Train LSTM**
   - embed token IDs into dense vectors
   - feed sequences into an LSTM (or stacked LSTMs / BiLSTMs)
   - output layer: sigmoid activations for multi-label classification
   - loss function: binary cross-entropy
5. **Evaluate**
   - metrics like Precision@K, Recall@K, F1-score per hashtag
   - inspect confusion patterns (hashtags frequently confused with each other)
6. **Export artifacts**
   - save model weights (`model_lstm.h5`)
   - save `Tokenizer` and `MultiLabelBinarizer` as pickles

---

## Suggested Charts and Analytics

Although the repository does not ship notebooks or dashboards, here are recommended charts and analyses to build around this model:

1. **Label distribution chart**
   - Bar chart of hashtag frequencies (before training)
   - Helps understand class imbalance
2. **Precision/Recall vs. K**
   - Line chart: K on x-axis (1, 3, 5, 10)
   - Precision@K and Recall@K on y-axis
   - Shows trade-off between returning more hashtags and maintaining quality
3. **Per-label F1 scores**
   - Bar chart across hashtags
   - Highlights which hashtags are easy/hard for the model
4. **Confusion heatmap**
   - For popular hashtags, plot co-occurrence matrix of predicted vs. true
   - Reveals semantically similar tags the model confuses
5. **Tweet-level error analysis**
   - Table or scatter plot of:
     - tweet length vs. prediction correctness
     - presence of URLs/mentions vs. error rates

These can be implemented in a separate notebook using pandas, matplotlib, seaborn, or Plotly.

---

## Logging and Monitoring (Ideas)

The current app is intentionally minimal and does **not** yet include logging/monitoring, but here is how you can extend it:

- **Request logging**
  - log incoming tweets (redacted/anonymized) and predicted hashtags
  - store in a local SQLite or cloud database for later analysis
- **Performance logging**
  - track latency per request (time to predict)
  - monitor model loading time at startup
- **Feedback loop**
  - add a simple thumbs-up / thumbs-down or “correct hashtags” field on the UI
  - store user feedback and actual usage to retrain or fine-tune the model

---

## Extending the Project

Some concrete extension ideas:

- **REST API**
  - add `/api/predict` endpoint that accepts JSON:
    - `{"text": "your tweet here", "top_k": 5}`
  - returns JSON:
    - `{"hashtags": ["#ai", "#python", ...]}`
- **CLI tool**
  - create a CLI script that reads tweets from stdin or a file, outputs hashtags
- **Batch scoring**
  - script to read a CSV of tweets and write predictions back to a CSV
- **Improved text preprocessing**
  - custom tokenization for hashtags, emojis, URLs, user mentions
  - language detection and route to language-specific models
- **UI improvements**
  - better styling, responsive layout
  - highlight hashtags as clickable chips
  - copy-to-clipboard button for predicted hashtags

---

## Roadmap / Future Improvements

Potential directions for contributors:

- add training scripts and example notebooks
- add evaluation scripts with metrics and charts
- add API endpoints and OpenAPI/Swagger documentation
- integrate basic logging + monitoring for predictions
- add Dockerfile and docker-compose setup for easy deployment
- support multiple models (e.g., transformer-based models) behind a unified interface

---

## Contributing

Contributions are welcome! Suggested flow:

1. Fork the repository
2. Create a feature branch from the latest `main`
3. Follow a clean, modular structure similar to the existing `hashtag_predictor` package
4. Use clear, conventional commits (e.g. `feat(api): add predict endpoint`, `refactor(core): simplify prediction pipeline`)
5. Open a Pull Request with:
   - description of changes
   - screenshots/plots if you modified UI or evaluation code

---

## License

Specify the project license here (e.g., MIT, Apache-2.0). If you add a `LICENSE` file, reference it from this section.
