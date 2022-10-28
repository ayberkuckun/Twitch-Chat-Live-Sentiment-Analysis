from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as soup
import time
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

driver.get("https://www.twitch.tv/montanablack88")

# ScAnimatedNumber-sc-acnd2k-0
# CoreText-sc-cpl358-0

try:
    view_count = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".ScAnimatedNumber-sc-acnd2k-0.cIxmzd"))
    )
    _ = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "chat-line__message"))
    )
    print('[LOG] Found all required elements')
    # chat = driver.find_element(By.CSS_SELECTOR, '.chat-line__message')
    # chat = driver.find_element(
    #     By.CSS_SELECTOR, '.Layout-sc-nxg1ff-0.aleoz.chat-scrollable-area__message-container :last-child')
    # print(chat.text)
    while True:
        html = driver.page_source
        page_soup = soup(html, features='html.parser')
        last_message = page_soup.find_all(
            'div', {'class': 'chat-line__message'})[-1].get_text()
        view_count = page_soup.find(
            'span', {'class': ['ScAnimatedNumber-sc-acnd2k-0', 'cIxmzd']}).get_text()
        print("[Last Message/View Count]:", last_message, view_count)
        time.sleep(1)


except Exception as e:
    print(e)
    driver.quit()


driver.quit()
