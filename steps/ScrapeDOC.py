from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

def Scrape():  
    halls = ['allison', 'sargent', 'plexWest', 'plexEast', 'elder']
    
    excludes = [
        " Cubed Cantaloupe ",
      " Cubed Pineapple ",
      " Cubed Honeydew ",
      " 2% Greek Plain Yogurt ",
      " Low Fat Vanilla Yogurt ",
      " Low Fat Strawberry Yogurt ",
      " Oats 'n Honey Granola ",
      " Raisins ",
      " Light Cream Cheese ",
      " Sunflower Spread ",
      " Grape Jelly ",
      " Strawberry Preserves ",
      " Butter ",
      " Fruit Cup ",
      " Cucumber Beet Salad ",
    ]

    output = {
    'allison': {
        'dinner': []
    },
    'elder': {
        'breakfast': [],
        'lunch': [],
        'dinner': []
    },
    'plexWest': {
        'breakfast': [],
        'lunch': [],
        'dinner': []
    },
    'plexEast': {
        'lunch': [],
        'dinner': []
    },
    'sargent': {
        'breakfast': [],
        'lunch': [],
        'dinner': []
    },
}
    # DineOnCampus main URL
    url = 'https://dineoncampus.com/northwestern/whats-on-the-menu'
    # Setup webdriver and wait for page to load
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(12)

    for i, hall in enumerate(halls):

        hallsDiv = driver.find_element(By.ID, 'menu-location-selector')
        hallsDropdown = hallsDiv.find_element(By.CSS_SELECTOR, ":nth-child(2)")

        # Click the dropdown button to open the menu
        hallsButton = driver.find_element(By.ID, 'menu-location-selector__BV_toggle_')
        hallsButton.click()
        time.sleep(2)

        # Select the left main dropdown containing dining hall names
        locationsInnerList = hallsDropdown.find_element(By.CSS_SELECTOR, ":nth-child(1)")
        mainUL = locationsInnerList.find_element(By.CSS_SELECTOR, ":nth-child(2)")

        cssFinder = ":nth-child(" + str(i + 1) + ")"
        listItem = mainUL.find_element(By.CSS_SELECTOR, cssFinder)
        buttonItem = listItem.find_element(By.CSS_SELECTOR, ":nth-child(1)")

        buttonItem.click()
        time.sleep(5)

        meals = []
        # ADD BREAKFAST
        if hall in ['sargent', 'plexWest', 'elder']:
            meals.append(('breakfast', driver.find_element(By.XPATH, "//*[text()='Breakfast']")))
        # ADD LUNCH
        if hall != 'allison':
            meals.append(('lunch', driver.find_element(By.XPATH, "//*[text()='Lunch']")))
        # ADD DINNER
        meals.append(('dinner', driver.find_element(By.XPATH, "//*[text()='Dinner']")))

        for meal in meals:
            meal[1].click()
            time.sleep(10)
            content = driver.page_source
            doc = BeautifulSoup(content, 'html.parser')

            # Print out text of each <strong> tag - these contain the entree/option names
            tags = doc.find_all('strong')
            for tag in tags:
                output[hall][meal[0]].append(tag.text)
    
    driver.quit()

    with open('/Users/joshprunty/Desktop/DHEmailer/data/meals.json', 'w') as file:
        json.dump(output, file)