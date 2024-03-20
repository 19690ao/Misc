import os
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
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
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.execute_script("window.scrollTo(10, 500);")
        # Execute JavaScript to click the element
        # time.sleep(1)
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath_expression))
        )
        # Use JavaScript to trigger the hover event
        # driver.execute_script("arguments[0].dispatchEvent(new Event('mouseover'));", element)
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
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

def change_zoom(driver, zoom=1):
    driver.execute_script(f"document.body.style.zoom='{zoom}';")

def main():
    driver = initialize_chrome_driver("https://www.streetfighter.com/6/buckler/stats/dia")
    # Wait for an element to be clickable and then click it
    click_element_when_ready(driver, "CybotCookiebotDialogBodyButtonDecline")
    click_element_by_xpath(driver, "//li[contains(text(), 'Control type total')]")
    click_element_by_xpath(driver, "//article[contains(@id, 'dia')]")
    click_element_by_xpath(driver, "//ul[contains(@class, 'league_nav_league_select')]//img[contains(@alt, 'MASTER')]/ancestor::span[contains(@class, 'league_nav_image')]")
    # Zoom out to ensure all elements are visible
    change_zoom(driver, 0.5)
    table = driver.find_element(By.CLASS_NAME, "dia_table_inner__r5tna")
    print(table)
    # If the table is found, proceed to extract its information
    rows = table.find_elements(By.TAG_NAME, "tr")
    output_list = [[],[]]
    
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        name = row.find_element(By.TAG_NAME, "th").text
        output_list[0].append(name)
        output_list.append([])
        # print(row_num, len(cols), end=' ')
        for col in cols:
            # Extract and print the text from each cell
            if not col.text: continue
            if col.text == '-': break
            # print(col.text, end=',')
            output_list[-1].append(round(float(col.text)/10, 4))
        print(output_list[-1])
    name_indices = {name: index for index, name in enumerate(output_list[0])}
    driver.get("https://www.streetfighter.com/6/buckler/en/stats/usagerate")
    click_element_by_xpath(driver, "//ul[contains(@class, 'league_nav_league_select')]//img[contains(@alt, 'MASTER')]/ancestor::span[contains(@class, 'league_nav_image')]")
    change_zoom(driver, 0.5)
    # Find the unordered list by its class name
    ul_element = driver.find_element(By.XPATH, "//div[contains(@class, 'usagerate_league__MObUs') and .//img[@alt='MASTER']]/ul[@class='usagerate_character__Bju8S']")
    # Find all list items within the unordered list
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    # Iterate over each list item to extract the name and percentage
    output_list[1] = [None]*len(output_list[0])
    for li in li_elements:
        # Extract the name from the <dt> element
        name = li.find_element(By.TAG_NAME, "dt").text
        
        # Extract the percentage from the <span class="usagerate_play_rate__aChNq"> element
        percentage = li.find_element(By.CLASS_NAME, "usagerate_play_rate__aChNq").text
        if not name or not percentage: continue
        index = name_indices[name]
        print(f"Name: {name}, Percentage: {percentage}")
        output_list[1][index] = round(float(percentage)/100, 5)
    assert len(output_list[0]) == len(output_list[1])
    # Close the browser
    driver.quit()

    
if __name__ == "__main__":
    main()