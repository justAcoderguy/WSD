from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

class WebDriver():
    """
        Return Chrome Webdriver
    """
    def get_chrome_driver(self):
        options=Options()
        options.headless = True
        try:
            # Runs if there is a Chrome Webdriver present on the system 
            driver = webdriver.Chrome(f"{str(BASE_DIR)}" + "/chromedriver", options=options)
        except Exception:
            # Installs webdriver for you
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        
        return driver