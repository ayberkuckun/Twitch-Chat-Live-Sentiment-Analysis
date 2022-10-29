from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
sentiment_task = pipeline("sentiment-analysis", model=model)
analyzer = SentimentIntensityAnalyzer()

def sentimentAnalyzeSentence(sentence):
    scores = analyzer.polarity_scores(sentence)
    return scores