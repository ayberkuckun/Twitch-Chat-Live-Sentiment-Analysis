from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as soup
import time
from model import sentimentAnalyzeSentence

TWITCH_USERNAME = 'dota2ti' # channel for analysis
TICK_FREQUENCY = 1.0 # message pulling rate

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f"https://www.twitch.tv/{TWITCH_USERNAME}")

    last_tuple = 'text'
    while True:
        html = driver.page_source
        page_soup = soup(html, features='html.parser')
        tuples = page_soup.find_all(
            'div', {'class': 'chat-line__message'})
        tuples = [m.get_text() for m in tuples]
        idx = 0
        try:
            idx = tuples.index(last_tuple)
            tuples = tuples[idx+1:]
        except:
            pass
        if len(tuples) > 0:
            last_tuple = tuples[-1]
            for tple in tuples:
                message = tple.split(':')[1]
                message = message.strip()
                if message != '':
                    sentiment = sentimentAnalyzeSentence(message)

                    # neutral 1.0 means 0 information about the messages sentiment
                    # good to discard these messages
                    if sentiment["neu"] != 1.0:
                        print(message)
                        print(str(sentiment))
                        print("\n")
        time.sleep(TICK_FREQUENCY)
