from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# settings
classifieds_link = 'https://classifieds.ksl.com/search/Auto-Parts-and-Accessories/Wheels-and-Tires-Cars'
seconds_to_wait_between_checking = 30


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')

# windows
driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver.exe')

def get_first_listing_info():
    driver.get(classifieds_link)
    link = driver.find_element_by_css_selector('#search-results > div > section > div > div > section:nth-child(4) > a').get_attribute('href')
    title = driver.find_element_by_css_selector('#search-results > div > section > div > div > section:nth-child(4) > a > div.listing-item-info > h2 > div').text
    driver.find_element_by_css_selector()
    return(link,title)

listing_info = get_first_listing_info()
get_first_listing_temp = listing_info[0]
title = listing_info[1]
print('first listing title: ' + title + " Link: " + get_first_listing_temp)

check_count = 0

while True:
    check_count += 1
    time.sleep(seconds_to_wait_between_checking)
    print("Checking to see if there is a new ad, this is attempt number: " + str(check_count))
    listing_info = get_first_listing_info()
    first_listing_link = listing_info[0]
    title = listing_info[1]
    if get_first_listing_temp != first_listing_link:
        print("There is a new ad! Title: " + title + ' Link: ' + first_listing_link)
        break
