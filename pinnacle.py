from selenium.webdriver.common.by import By
import time
from db import Database
from webdriver import WebDriver


class Pinnacle:
    def __init__(self) -> None:
        self.path = 'https://www.pinnacle.com/en/soccer/england-premier-league/matchups#period:0'
        self.driver = WebDriver().get_chrome_driver()

    def _make_request(self):
        self.driver.get(self.path)
        time.sleep(4)
        # Getting the content block
        content_block = self.driver.find_elements(By.CSS_SELECTOR,".contentBlock")[1:]
        return content_block

    def _extract_information(self, contents):
        content_block_square = contents[1]
        children = content_block_square.find_elements(By.XPATH, "./*")
        matches = {}
        # Initial Key (containing date)
        key = children[0].text.split("\n")[0]
        for child in children[1:]:
            if(child.get_attribute("class") != "style_dateBar__1dI_9"):
                if matches.get(key):
                    matches[key].append(child.text)
                else:
                    matches[key] = [child.text]
            elif(child.get_attribute("class") == "style_dateBar__1dI_9"):
                key = child.text.split("\n")[0]
        return matches

    def _validate_data(self, matches):
        updated_matches = []

        for value in matches.values():
            for match in value[1:]:
                try:
                    match = match.split('\n')
                    home_team = match[0]
                    away_team = match[1]
                    H, D, A = match[3], match[4], match[5]
                    _match = {
                        "home_team": home_team, 
                        "away_team": away_team, 
                        "H": H,
                        "D": D,
                        "A": A
                        }
                    updated_matches.append(_match)
                except Exception:
                    # 'Home Teams (6)' Edge case
                    pass

        return updated_matches

    def database_insert(self, data):
        table_name = "pinnacle"
        create_script = ''' CREATE TABLE IF NOT EXISTS pinnacle (
                                            id          serial PRIMARY KEY,
                                            home        varchar(40) NOT NULL,
                                            away        varchar(40) NOT NULL,
                                            H           real NOT NULL,
                                            D           real NOT NULL,
                                            A           real NOT NULL) '''
        insert_script  = 'INSERT INTO pinnacle (home, away, H, D, A) \
                            VALUES (%s, %s, %s, %s, %s)'
        insert_values = []
        for match in data:
            insert_values.append((
                match['home_team'], match['away_team'], match['H'], match['D'], match['A']))
        # Calling Database function
        Database().insert_data(
            table_name, create_script, insert_script, insert_values
        )

    def run(self):
        try:
            content = self._make_request()
            matches = self._extract_information(content)
            return self._validate_data(matches)
        except Exception as e:
            print(e)
        finally:
            self.driver.close()



########## To Print Pinnacle Scraped Data #########

if __name__ == "__main__":
    obj = Pinnacle()
    data = obj.run()
    #print(data)

    try:
        # Storing to database
        obj.database_insert(data)
    except Exception as e:
        print(e)
