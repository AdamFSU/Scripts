import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import pandas as pd

firefox_options = Options()
# firefox_options.headless = True

shoe_size = []

while True:
    entry = input("What size would you like to filter for? (enter each size one at a time, once "
                  "finished press ENTER again)\n"
                  "Only increments of 0.5 will be accepted: ")
    if entry == '':
        break
    else:
        try:
            test_number = float(entry)
            if test_number % 0.5 != 0 or test_number > 20 or test_number < 0:
                raise ValueError("The value you entered is not an accepted format, it will be excluded "
                                 "from affecting search results, enter a new number")
            else:
                shoe_size.append(test_number)
        except ValueError:
            print("The value you entered is not an accepted format, it will be excluded from affecting search results")

while True:
    entry2 = input("What is the max price of the shoe, of the sizes you selected, that you will be willing to "
                   "purchase (Enter a 2 or 3 digit integer value: ")

    try:
        max_price = int(entry2)
        break
    except ValueError:
        print("The value you entered is not an accepted format, please enter in a proper value.\n")

# Test that this is the correct path!
data_frame = pd.read_csv(sys.path.append(os.path.join(os.path.dirname(__file__), "stockx_results.csv")))
# print(sys.path.append(os.path.join(os.path.dirname(__file__), "stockx_results.csv")))

links_list = list(data_frame['links'])

distilled_req_list = []

with webdriver.Firefox(options=firefox_options) as driver:
    # website to scrape
    for link in links_list:
        driver.get(link)

        # webDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="select-control '
        # 'shoe-size"]')))

        driver.find_element_by_xpath('//button[@type="button"][@title="All"]').click()
        driver.implicitly_wait(3)
        drop_downs = driver.find_element_by_xpath('//li[@class="select-option"]')
        for drop_down in drop_downs:
            dd = drop_down.find_element_by_xpath('//div[@class="inset"]')
            print(dd.find_element_by_xpath('//div[@class="subtitle"]').text)
