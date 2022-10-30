from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as soup
import time
from producer import init_producer, send_message
import argparse

TICK_FREQUENCY = 1.0  # message pulling rate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--channel', '-c',
        type=str,
        help='Twitch Channel Name',
    )
    args = parser.parse_args()

    TWITCH_USERNAME_LIST = [args.channel]  # channel for analysis


    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    producer = init_producer()

    drivers = []
    for channel in TWITCH_USERNAME_LIST:
        drivers.append((webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options), channel))
        drivers[-1][0].get(f"https://www.twitch.tv/{channel}")

    last_tuple = 'text'
    while True:
        for driver, channel in drivers:
            html = driver.page_source
            page_soup = soup(html, features='html.parser')
            tuples = page_soup.find_all(
                'div', {'class': 'chat-line__message'})
            tuples = [m.get_text() for m in tuples]
            idx = 0
            try:
                idx = tuples.index(last_tuple)
                tuples = tuples[idx + 1:]
            except:
                pass
            if len(tuples) > 0:
                last_tuple = tuples[-1]
                for tple in tuples:
                    message = tple.split(':')[1]
                    message = message.strip()
                    if message != '':
                        send_message(producer, channel, message)  # sends message to kafka

        time.sleep(TICK_FREQUENCY)
