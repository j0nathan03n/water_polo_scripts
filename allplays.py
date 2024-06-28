from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import os
import logging
import glob


def labelGame(dataframe):
    print(type(dataframe["Team"]))
    team_list = dataframe["Team"]
    teams_series = pd.Series(team_list.unique())
    teams = teams_series.str.cat(sep = " ")
    dataframe["teams_in_game"] = teams
    print(dataframe.head())
    return dataframe

def combineCsv(path):
    csv_files = glob.glob(os.path.join(path, '*.csv'))
    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
    concatenated_df = pd.concat(dataframes, ignore_index=True)
    output_file = 'concatenated_plays.csv'
    concatenated_df.to_csv(output_file, index=False)


def main():
    file_path = os.getcwd() + '/url_games.txt'
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]

    for index,url in enumerate(lines):

        # # Set up WebDriver
        driver = webdriver.Chrome()  # or use webdriver.Firefox() for Firefox
 
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
        web_df = pd.concat(all_data, ignore_index=True)
        final_df = labelGame(web_df) # add the teams as a column in the csv

        # Export to CSV
        final_df.to_csv(f'data_{index}.csv', index=False)

        # Close the browser
        driver.quit()
    combineCsv(os.getcwd())




logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        main()
    except Exception as error_message:
        logger.exception(f"Error: Uncaught exception: {error_message} caused script to exit")
        exit(1)