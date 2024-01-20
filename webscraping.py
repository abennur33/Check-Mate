import time
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import os

# Set the current working directory to the directory of your Python script
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)


options = Options()
options.add_argument("--headless")  # No GUI
#s = Service('geckodriver')
s = webdriver.FirefoxService(executable_path='geckodriver.exe')
driver = webdriver.Firefox(service=s)

driver.get('https://www.factcheck.org/search/#gsc.tab=0')

time.sleep(2)



driver.quit()