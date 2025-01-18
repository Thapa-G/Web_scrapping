from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import pandas as pd
import os

# Initialize the WebDriver
driver = webdriver.Chrome()

cars_num = 0
links = []  # Create a list to store the href values

# Scrape the links from multiple pages
for i in range(4):
    try:
        driver.get(f"https://www.baysidebrothersmotors.com.au/USED-CAR-IN-VERMONT/pagenum-{i}")
        time.sleep(15)  # Allow the page to load fully
        
        elements = driver.find_elements(By.CLASS_NAME, 'search_item')
        for element in elements:
            try:
                link = element.find_element(By.CLASS_NAME, 'search_title').find_element(By.TAG_NAME, 'a')
                href = link.get_attribute("href")
                if href:  # Ensure href is not None or empty
                    links.append(href)  # Add the link to the list
            except NoSuchElementException:
                print(f"Element not found on page {i}. Continuing...")
    except WebDriverException as e:
        print(f"Error accessing page {i}: {e}. Skipping...")
df = pd.DataFrame(links, columns=['Link'])
df.to_csv('Scrapped_data_copy.csv', index=False)

for link in links:
    try:
        driver.get(link) 
        time.sleep(5)
        
        try:
            Details = driver.find_element(By.ID, 'details-vehicle-info-features-Body')
            location = driver.find_element(By.ID, 'details-sidebar-main-yardlocation')
            
            html_data = Details.get_attribute('outerHTML')
            location_data = location.get_attribute('outerHTML')
            combined_data = f"{html_data}\n\n{location_data}"
            with open(f"html_data/car_{cars_num}.html", "w", encoding="utf-8") as f:
                f.write(combined_data)
            cars_num += 1
        except NoSuchElementException as e:
            print(f"Some elements not found on {link}: {e}. Skipping this link...")
    except WebDriverException as e:
        print(f"Error accessing link {link}: {e}. Skipping...")

# Close the WebDriver
driver.close()
