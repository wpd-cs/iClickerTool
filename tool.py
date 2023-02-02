import os
import time
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import randint, uniform

def worker(username, password):
    # Function to sign in iClicker using provided credentials and
    # check-in to a specified class

    print(username + " zombie starting")

    location = dict({
        "latitude": uniform(33.882285, 33.882349),
        "longitude": uniform(-117.882795, -117.882754),
        "accuracy": 100
    })

    # Create incognito Google Chrome instance
    capabilities = DesiredCapabilities().CHROME
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument('--headless')

    prefs = {
        'profile.default_content_setting_values':
        {
            'notifications': 1,
            'geolocation': 1
        },
        'profile.managed_default_content_settings':
        {
            'geolocation': 1
        },
    }

    chrome_options.add_experimental_option('prefs', prefs)
    capabilities.update(chrome_options.to_capabilities())
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", location)

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
    print(username + " clicked the sign-out button")

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
