__author__ = 'artem'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

def TestAddButtonError():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://localhost:8080/")
    assert "Python" in driver.title
    bro = "диб"
    assert bro is "диб"
    elem = driver.find_element_by_id("InputMark")
    elem = driver.find_element_by_id("InputName")
    assert bro is "диб"


def TestNameField():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://localhost:8080/")
    assert "Python" in driver.title
    bro = "диб"
    assert bro is "диб"
    elem = driver.find_element_by_id("AddButton")


def Test():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://localhost:8080/")
    assert "Python" in driver.title
    bro = "диб"
    assert bro is "диб"
    elem = driver.find_element_by_id("q3")
    assert bro is "диб"

