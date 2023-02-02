import os
import time
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from random import randint

def worker(username, password):
    # Function to sign in iClicker using provided credentials and
    # check-in to a specified class

    print(username + " zombie starting")

    # Create incognito Google Chrome instance
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Go to iClicker login screen
    driver.get('https://student.iclicker.com/#/login')
    
    # Input credentials
    username_input = driver.find_element(By.ID, "userEmail")
    password_input = driver.find_element(By.ID, "userPassword")
    
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Allow random login times
    time.sleep(randint(5, 16))
    
    # Submit the form
    password_input.send_keys(Keys.RETURN)
    print(username + " logged in")
    
    # Wait for the page to load / allow random check-in times
    time.sleep(randint(5, 15))

    # Click into the specified class
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/main/div[3]/ul[1]/li/a/label[text()='CPSC 462-05. Object Oriented Software Design']").click()
    print(username + " clicked into the class")
    
    # Allow random join times
    time.sleep(randint(4, 14))

    # Check if Join button is displayed
    if driver.find_element(By.ID, "btnJoin").is_displayed():
        # Click it if so
        driver.find_element(By.ID, "btnJoin").click()
        print(username + " clicked the Join Button")

        # If join was successful, we may need an extra action (a button press or something), before continuing to logout

    else:
        # Else let the user know that it's not displayed, then do nothing
        print(username + "'s Join button is not available at the moment")

    # Allow random back-out times
    time.sleep(randint(7, 12))

    # Hit the Back button to go back to class list view
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/nav-bar/div/div/div/button").click()
    print(username + " went back to the class list view")

    # Allow random back out times
    time.sleep(randint(3, 10))

    # Hit the hamburger menu
    driver.find_element(By.ID, "menu-hamburger-container").click()
    print(username + " clicked the hamburger menu")

    # Allow hamburger menu to expand
    time.sleep(randint(3, 10))

    # Click the Sign Out button
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/div[2]/ul/li[4]/button").click()
    print(username + " clicked the signout button")

    # Allow for proper logout
    time.sleep(randint(5, 8))
    print(username + " zombie terminating")

    # Quit Chrome instance
    driver.quit()

if __name__ == '__main__':
    # Main function

    with open('creds.txt') as f:
        for line in f:
            username, password = line.strip().split(', ')
            t = threading.Thread(target=worker, args=(username, password))
            t.start()
