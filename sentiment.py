from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
sentiment_task = pipeline("sentiment-analysis", model=model)
analyzer = SentimentIntensityAnalyzer()

def sentimentAnalyzeSentence(sentence):
    scores = sentiment_task(sentence)
    sentiment = singleSentimentScore(scores)
    return sentiment

def singleSentimentScore(scores):
    label = scores[0]["label"]
    score = scores[0]["score"]
    if label == "Neutral":
        return 0.0
    elif label == "Positive":
        return score
    elif label == "Negative":
        return -score
