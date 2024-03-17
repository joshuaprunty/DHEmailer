from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import boto3


def Scrape():

    # List of Dining Halls as strings
    halls = ['allison', 'sargent', 'plexWest', 'plexEast', 'elder']

    # JSON Wireframe for output.
    output = {
        'allison': {
            'breakfast': [],
            'lunch': [],
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
        }
    }

    # DineOnCampus URL
    url = 'https://dineoncampus.com/northwestern/whats-on-the-menu'

    # Setup webdriver.
    # Get URL.
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for page to load
    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.ID, "menu-location-selector"))
    )

    # Loop over five dining halls
    for i, hall in enumerate(halls):

        # Find the dropdown listing dining halls
        hallsDiv = driver.find_element(By.ID, 'menu-location-selector')
        hallsDropdown = hallsDiv.find_element(By.CSS_SELECTOR, ":nth-child(2)")

        # Find and Click the dropdown button to open the menu, wait for load
        hallsButton = driver.find_element(By.ID, 'menu-location-selector__BV_toggle_')
        hallsButton.click()

        # Wait for load
        WebDriverWait(hallsDiv, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "show"))
        )

        # Find the left main dropdown containing dining hall names
        locationsInnerList = hallsDropdown.find_element(By.CSS_SELECTOR, ":nth-child(1)")
        mainUL = locationsInnerList.find_element(By.CSS_SELECTOR, ":nth-child(2)")

        # Find the appropriate hall button in the dropdown via iterator i.
        # Click the button, wait for load.
        cssFinder = ":nth-child(" + str(i + 1) + ")"
        listItem = mainUL.find_element(By.CSS_SELECTOR, cssFinder)
        buttonItem = listItem.find_element(By.CSS_SELECTOR, ":nth-child(1)")
        buttonItem.click()

        # Get Main-Content div, mainly for wait XPATHs
        mainContent = driver.find_element(By.ID, "main-content")

        # Wait for load, on either open or closed hall
        WebDriverWait(mainContent, 10).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//div/div/div[2]/div[3]/div/div[1]/div/div[1]/ul")),
                EC.presence_of_element_located((By.XPATH, "//div/div/div[2]/div[@class='row closed-copy']"))
            )
        )

        # Array will hold tuples (meal identifier, button element for meal).
        meals = []

        # Add Breakfast tuple
        meals.append(('breakfast', driver.find_elements(By.XPATH, "//*[text()='Breakfast']")))
        # Add Lunch tuple
        meals.append(('lunch', driver.find_elements(By.XPATH, "//*[text()='Lunch']")))
        # Add Dinner tuple
        meals.append(('dinner', driver.find_elements(By.XPATH, "//*[text()='Dinner']")))

        # Loop through meals offered at this hall
        for meal in meals:
            # Click button element, long wait for load.
            if meal[1]:
                meal[1][0].click()

                # Wait for menu load
                WebDriverWait(mainContent, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div/table"))
                )

                # We're now on the page holding our desired meal data.
                # Initialize BS for this page
                content = driver.page_source
                doc = BeautifulSoup(content, 'html.parser')
                # <Strong> tags hold each dish name - add content of each to output.
                tags = doc.find_all('strong')
                for tag in tags:
                    output[hall][meal[0]].append(tag.text)

    # Kill the webdriver
    driver.quit()

    # Output now holds our full scraped data - write it as-is to meals.json.
    json_data = json.dumps(output)

    s3_client = boto3.client('s3')

    bucket_name = 'diningscraper'
    key = 'usrmeal/meals.json'  

    # Write the JSON data to meals.json in your S3 bucket
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=json_data, ContentType='application/json')

def lambda_handler(event, context):
    Scrape()
    return {
        'statusCode': 200,
        'body': json.dumps('Scrape Successful!')
    }
