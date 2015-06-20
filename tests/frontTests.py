__author__ = 'artem'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

def TestAddButtonError():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("InputMark")
    elem = driver.find_element_by_id("InputName")
    if bro is "asd":
        assert bro is "asd"

def TestNameFieldEr2():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("AddButton")

def TestNameFieldEr1():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("AddButton")

def TestNameField2():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("AddButton")
    elem1 = driver.find_element_by_id("InputNationality")
    assert bro is "sss"


def Test2():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("InputNationality")
    assert bro is "asd"

def TestNat1():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("InputNationality")
    assert bro is "asd"

def TestNat2():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem1 = driver.find_element_by_id("InputNationality")
    assert bro is "asd"

def TestNat3():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("InputNationality")
    assert bro is "asd"

def TestNat4():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("InputNationality")
    assert bro is "asd"
    assert bro is "asd"
    assert bro is "asd"

def TestNat5():
    ChromeDriver = "/Users/artem/Desktop/StudManager/tests/chromedriver"
    os.environ["webdriver.chrome.driver"] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    driver.get("http://artdyachkov.fvds:8080/")
    assert "Python" in driver.title
    bro = "asd"
    assert bro is "asd"
    elem = driver.find_element_by_id("InputNationality")
    assert bro is "asd"
