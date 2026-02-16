from flask import Blueprint, render_template, request

from .prediction import predict_hashtags_top_k


main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def home():
    hashtags = []
    tweet_text = ""
    if request.method == "POST":
        tweet_text = request.form.get("tweet", "")
        hashtags = predict_hashtags_top_k(tweet_text)
    return render_template("index.html", tweet=tweet_text, hashtags=hashtags)

