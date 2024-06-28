from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import os

#file_path = '/Users/jonathanoen/Desktop/sports_scripts/url_games.txt'
file_path = os.getcwd() + '/url_games.txt'
with open(file_path, 'r') as file:
    lines = [line.strip() for line in file]

for index,url in enumerate(lines):

    # Set up WebDriver
    driver = webdriver.Chrome()  # or use webdriver.Firefox() for Firefox
    #driver.get('https://scores.6-8sports.com/unity/leagues/faa5368a-fdc8-4350-9764-8e9eb5098d5e/conferences/cc2d0640-d6bb-4565-803b-7d7282649a85/schedule/games/e9b7e228-2765-4f16-86c2-37ae93f06ccc/play-by-play?is_shared=True')

    # Open the website
    #rl = 'https://scores.6-8sports.com/unity/leagues/faa5368a-fdc8-4350-9764-8e9eb5098d5e/conferences/cc2d0640-d6bb-4565-803b-7d7282649a85/schedule/games/5840ba38-32eb-4fde-8957-132ce8a5f23a/play-by-play'
    #url = 'https://scores.6-8sports.com/unity/leagues/faa5368a-fdc8-4350-9764-8e9eb5098d5e/conferences/cc2d0640-d6bb-4565-803b-7d7282649a85/schedule/games/c0fb1e95-e801-4400-bd75-d6c807fe8ee9/play-by-play'

    print(url)
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # Click all "arrow-down" buttons to expand the tables
    try:
        # Locate all elements with the specified class name
        arrow_buttons = driver.find_elements(By.CSS_SELECTOR, 'arrow-down.ng-star-inserted')
        print(arrow_buttons)
        for button in arrow_buttons:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)  # Delay to ensure the table expands properly
            print("buttons_clicked")
    except Exception as e:
        print(f"An error occurred: {e}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table')


    # After expanding all tables, grab the data
    tables = driver.find_elements(By.TAG_NAME, 'table')
    print(tables)
    # Process and export data
    all_data = []
    for table in tables:
        table_html = table.get_attribute('outerHTML')
        df = pd.read_html(table_html)[0]
        all_data.append(df)

    # Concatenate all data into a single DataFrame
    final_df = pd.concat(all_data, ignore_index=True)
    # 

    # Export to CSV
    final_df.to_csv(f'data_{index}.csv', index=False)

    # Close the browser
    driver.quit()
