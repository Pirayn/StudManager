__author__ = 'artem'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
os.environ["webdriver.chrome.driver"] = ChromeDriver

driver = webdriver.Chrome(ChromeDriver)

driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()