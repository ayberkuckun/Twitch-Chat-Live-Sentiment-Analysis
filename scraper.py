from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

driver.get("https://www.twitch.tv/tolkinlol")

# ScAnimatedNumber-sc-acnd2k-0
# CoreText-sc-cpl358-0

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".ScAnimatedNumber-sc-acnd2k-0.cIxmzd"))
    )
    # view_count = element.find
    print(element.text)
except:
    print("Failed")
    driver.quit()


driver.quit()
