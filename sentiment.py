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
    return scores["pos"]-scores["neg"]
