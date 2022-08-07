from selenium.webdriver.common.by import By
import time
from db import Database
from webdriver import WebDriver

class SMarkets:
    def __init__(self) -> None:
        self.path = 'https://smarkets.com/listing/sport/football/england-premier-league'
        self.driver = WebDriver().get_undetected_chrome_driver()

    def _make_request(self):
        self.driver.get(self.path)
        time.sleep(10)

        # Getting the events
        events = self.driver.find_elements(By.CSS_SELECTOR,".item-tile")
        number_of_matches = len(events)
        if number_of_matches == 0:
            raise Exception("No matches could be found")
        return number_of_matches
       

    def _extract_information(self, count):
        matches = []
        for i in range(1, count):
            match = {}
            match["home_team"] = self.driver.find_element(By.XPATH,f'//*[@id="main-content"]/main/div[2]/ul/li[{i}]/div[1]/a[2]/div/div[1]/span').text
            match["away_team"] = self.driver.find_element(By.XPATH,f'//*[@id="main-content"]/main/div[2]/ul/li[{i}]/div[1]/a[2]/div/div[2]/span').text
            match["for_home"] = self.driver.find_element(By.XPATH,f'//*[@id="main-content"]/main/div[2]/ul/li[{i}]/div[2]/span[1]/div/span[1]/span[1]').text
            match["against_home"] = self.driver.find_element(By.XPATH,f'//*[@id="main-content"]/main/div[2]/ul/li[{i}]/div[2]/span[1]/div/span[2]/span[1]').text
            match["for_draw"] = self.driver.find_element(By.XPATH,f'//*[@id="main-content"]/main/div[2]/ul/li[{i}]/div[2]/span[2]/div/span[1]/span[1]').text
            match["against_draw"] = self.driver.find_element(By.XPATH,f'//*[@id="main-content"]/main/div[2]/ul/li[{i}]/div[2]/span[2]/div/span[2]/span[1]').text
            match["for_away"] = self.driver.find_element(By.XPATH,f'//*[@id="main-content"]/main/div[2]/ul/li[{i}]/div[2]/span[3]/div/span[1]/span[1]').text
            match["against_away"] = self.driver.find_element(By.XPATH,f'//*[@id="main-content"]/main/div[2]/ul/li[{i}]/div[2]/span[3]/div/span[2]/span[1]').text
            matches.append(match)
        return matches

    def database_insert(self, data):
        table_name = "smarkets"
        create_script = ''' CREATE TABLE IF NOT EXISTS smarkets (
                                            id          serial PRIMARY KEY,
                                            home        varchar(40) NOT NULL,
                                            away        varchar(40) NOT NULL,
                                            H_for       real NOT NULL,
                                            H_against   real NOT NULL,
                                            D_for       real NOT NULL,
                                            D_against   real NOT NULL,
                                            A_for       real NOT NULL,
                                            A_against   real NOT NULL) '''
        insert_script  = 'INSERT INTO smarkets (home, away, H_for, H_against, D_for, D_against, A_for, A_against) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        insert_values = []
        for match in data:
            insert_values.append((
                match['home_team'], match['away_team'], match['for_home'], match['against_home'], match['for_draw'], match['against_draw'], match['for_away'], match['against_away']))
        # Calling Database function
        Database().insert_data(
            table_name, create_script, insert_script, insert_values
        )


    def run(self):
        try:
            count = self._make_request()
            return self._extract_information(count)
        except Exception as e:
            print(e)
        finally:
            self.driver.close()



########## To Print Smarkets Scraped Data #########

if __name__ == "__main__":
    obj = SMarkets()
    data = obj.run()
    # uncomment this to print matches data 
    # print(data)

    try:
        # Storing to database
        obj.database_insert(data)
    except Exception as e:
        print(e)
