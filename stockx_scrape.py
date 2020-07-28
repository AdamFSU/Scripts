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

with webdriver.Firefox(options=firefox_options) as driver:

    # website to scrape
    driver.get("https://stockx.com/")

    # find search bar and search for product

    search_bar = driver.find_element_by_name("q")
    search_bar.send_keys("air_jordan" + Keys.RETURN)

    page_number = 1

    # Initialize empty lists

    titles_list = []
    prices_list = []
    links_list = []

    ignore_exceptions = StaleElementReferenceException

    while True:

        # Explicit wait until an element is located on the page

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'dqBWTy')))
            driver.implicitly_wait(3)
        except StaleElementReferenceException:
            print("unable to wait for page load")
            driver.quite()
            break

        # Grab all HTML elements on page with item titles and item prices

        item_titles = driver.find_elements_by_class_name('hugwvm')
        item_prices = driver.find_elements_by_class_name('feUFro')
        item_links = driver.find_elements_by_xpath('//a[@style="color: black;"]')
        for link in item_links:
            links_list.append(link.get_attribute('href'))

        # Loop over the item_titles and item_prices

        for title in item_titles:
            titles_list.append(str(title.text).replace('\n', ''))
        for price in item_prices:
            prices_list.append(price.text)

        try:
            next_page = driver.find_element_by_xpath('//a[contains(@href, "page={page}")]'.format(page=page_number+1))
            next_page.click()
            page_number = page_number + 1
        except NoSuchElementException:
            print("page " + str(page_number+1) + " not found. Finishing scrape")
            driver.quit()
            break

    # print out scraped data and format it

    data_frame = pd.DataFrame(zip(titles_list, prices_list, links_list), columns=['Item Name', 'Price', 'links'])
    print(data_frame)
    data_frame.to_csv(sys.path.append(os.path.join(os.path.dirname(__file__), "stockx_results.csv")), index=False,
                      header=True)
