from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as soup
import time
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

twitch_username = 'hasanabi'
driver.get(f"https://www.twitch.tv/{twitch_username}")

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
                print(message)
    time.sleep(0.25)
