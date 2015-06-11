__author__ = 'artem'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

def TestBro1():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://localhost:8080/")
    assert "Python" in driver.title
    bro = "диб"
    assert bro is "диб"
    elem = driver.find_element_by_id("q11")
    assert bro is "диб"
    elem = driver.find_element_by_id("q1")


def TestBro2():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://localhost:8080/")
    assert "Python" in driver.title
    bro = "диб"
    assert bro is "диб"
    elem = driver.find_element_by_id("q2")


def TestBro3():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://localhost:8080/")
    assert "Python" in driver.title
    bro = "диб"
    assert bro is "диб"
    elem = driver.find_element_by_id("q3")
    assert bro is "диб"

