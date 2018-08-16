# Compenents for web scrapping

from selenium import webdriver
import sys
import os

#start headless mode,return driver for use
def headless_mode():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=800x600')
    driver_path = os.getcwd()+'/chromedriver'
    driver = webdriver.Chrome(executable_path = driver_path,chrome_options=options)
    return driver

#start normal mode,return driver for use    
def normal_mode():
    driver_path = os.getcwd()+'/chromedriver'
    driver = webdriver.Chrome(executable_path = driver_path)
    return driver

# locate the elements in the login page, input account and password and login
def login_xpath(driver,url,account_xpath,password_xpath,login_xpath,account_content,password_content):
    driver.get(url)
    account = driver.find_element_by_xpath(account_xpath)
    password = driver.find_element_by_xpath(password_xpath)
    login = driver.find_element_by_xpath(login_xpath)
    account.send_keys(account_content)
    password.send_keys(password_content)
    if isinstance(login,list):
        login[0].click()
    else:
        login.click()
    
