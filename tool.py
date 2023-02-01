import os
import time
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from random import randint

def worker(username, password):
    # Task

    print(username + " is logging in")
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://student.iclicker.com/#/login')
    
    username_input = driver.find_element(By.ID, "userEmail")
    password_input = driver.find_element(By.ID, "userPassword")
    username_input.send_keys(username)
    password_input.send_keys(password)
    
    # Submit the form
    password_input.send_keys(Keys.RETURN)
    
    # Wait for the page to load
    time.sleep(randint(7, 12))

    driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/main/div[3]/ul[1]/li/a/label[text()='CPSC 462-05. Object Oriented Software Design']").click()
    
    time.sleep(randint(8, 14))

    if driver.find_element(By.ID, "btnJoin").is_displayed() or driver.find_element(By.ID, "btnJoin").is_displayed():
        driver.find_element(By.ID, "btnJoin").click()
        print(username + " checked into class")
    else:
        print("Join button not available at the moment")

    time.sleep(randint(7, 12))
    driver.quit()

if __name__ == '__main__':
    # Main function

    with open('creds.txt') as f:
        for line in f:
            username, password = line.strip().split(', ')
            t = threading.Thread(target=worker, args=(username, password))
            t.start()
