# Twitch Chat Live Sentiment Analysis

- `scraper.py` scrapes messages live messages from twitch channels
- pushes messages to Kafka
- `test.py` will consume the messages, and will analyze the chat sentiment using `PySpark`
- broker & zookeper for Kafka can be run as containers
