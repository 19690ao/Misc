import os
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def initialize_chrome_driver(url, headless=False):
    options = Options()
    if headless:
        options.add_argument('--headless=new')

    # Initialize the WebDriver using webdriver_manager
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service, options=options)

    # Access the webpage
    driver.get(url)
    return driver

def click_element_when_ready(driver, element_id, wait_time=10, verbose=False):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        element.click()
        if verbose:
            print("Element clicked successfully.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def click_element_by_xpath(driver, xpath_expression, wait_time=10, verbose=False):
    """
    Clicks an element on the page using its XPath expression, waiting for the element to be clickable.

    :param driver: Selenium WebDriver instance.
    :param xpath_expression: XPath expression to locate the element.
    """
    try:
        # Wait for the element to be clickable
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath_expression))
        )
        
        # Execute JavaScript to click the element
        driver.execute_script("arguments[0].click();", element)
        if verbose:
            print("Element clicked successfully.")
        return True
    except Exception as e:
        print(f"An error occurred while clicking the element: {e}")
        return False

def get_all_elements_info(driver):
    """
    Returns a string with information about all elements on the current page.

    :param driver: Selenium WebDriver instance.
    :return: String with information about all elements.
    """
    elements_info = []
    try:
        # Find all elements on the page using the new method
        all_elements = driver.find_elements(By.XPATH, '//*')
        
        # Extract and return information about all elements
        for element in all_elements:
            try:
                tag_name = element.tag_name
                element_id = element.get_attribute('id')
                if element_id != '':
                    elements_info.append(f"Tag: {tag_name}, ID: {element_id}")
            except StaleElementReferenceException:
                print("Element is no longer attached to the DOM.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Join all elements' information into a single string
    return "\n".join(elements_info)

def write_to_file(lst, folder, filename):
    # Create directory if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Full path to the file
    file_path = os.path.join(folder, filename)

    # Open the file in write mode ('w')
    with open(file_path, 'w', encoding='utf-8') as file:
        # Write each item in the list to a new line in the file
        for item in lst:
            file.write(f"{item}\n")

def main():
    driver = initialize_chrome_driver("https://www.streetfighter.com/6/buckler/stats/dia")
    # Wait for an element to be clickable and then click it
    click_element_when_ready(driver, "CybotCookiebotDialogBodyButtonDecline")
    click_element_by_xpath(driver, "//li[contains(text(), 'Control type total')]")
    time.sleep(2)
    click_element_by_xpath(driver, "//li[.//span[contains(@class, 'league_nav_image__xFm_A')]]")
    print("Masters")
    time.sleep(3)
    info = get_all_elements_info(driver)
    #print(info)
    write_to_file([info], "output", "temp.txt")
    
    # Close the browser
    driver.quit()


if __name__ == "__main__":
    main()