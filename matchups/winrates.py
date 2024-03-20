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

def get_element_by(driver, category, expression, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_all_elements_located((category, expression))
        )
        return element[0]
    except Exception as e:
        print(f"An error occurred while getting the element: {e}")
        return None
    
def get_all_elements_by(driver, category, expression, wait_time=10):
    try:
        elements = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_all_elements_located((category, expression))
        )
        return elements
    except Exception as e:
        print(f"An error occurred while getting the element: {e}")
        return None

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
    rank = "MASTER"
    if False: rank = input("What Rank?\n>> ").upper()
    driver = initialize_chrome_driver("https://www.streetfighter.com/6/buckler/stats/dia")
    # Wait for an element to be clickable and then click it
    click_element_when_ready(driver, "CybotCookiebotDialogBodyButtonDecline")
    click_element_by_xpath(driver, "//li[contains(text(), 'Control type total')]")
    click_element_by_xpath(driver, "//article[contains(@id, 'dia')]")
    click_element_by_xpath(driver, f"//ul[contains(@class, 'league_nav_league_select')]//img[contains(@alt, '{rank}')]/ancestor::span[contains(@class, 'league_nav_image')]")
    # Zoom out to ensure all elements are visible
    change_zoom(driver, 0.5)
    table = get_element_by(driver, By.CLASS_NAME, "dia_table_inner__r5tna")
    rows = get_all_elements_by(table, By.TAG_NAME, "tr")

    output_list = [[],[]]
    
    for row in rows:
        cols = get_all_elements_by(row, By.TAG_NAME, "td")
        name = get_element_by(row, By.TAG_NAME, "th").text
        if not name: continue
        output_list[0].append(name)
        output_list.append([])
        for col in cols[1:]:
            # Extract and print the text from each cell
            if not col.text: continue
            if col.text == '-': break
            output_list[-1].append(str(round(float(col.text)/10, 4)))
        print(output_list[-1])
    name_indices = {name: index for index, name in enumerate(output_list[0])}
    driver.get("https://www.streetfighter.com/6/buckler/en/stats/usagerate")
    click_element_by_xpath(driver, f"//ul[contains(@class, 'league_nav_league_select')]//img[contains(@alt, '{rank}')]/ancestor::span[contains(@class, 'league_nav_image')]")
    change_zoom(driver, 0.5)
    # Find the unordered list by its class name
    ul_element = get_element_by(driver, By.XPATH, f"//div[contains(@class, 'usagerate_league__MObUs') and .//img[@alt='{rank}']]/ul[@class='usagerate_character__Bju8S']")
    # Find all list items within the unordered list
    li_elements = get_all_elements_by(ul_element, By.TAG_NAME, "li")
    # Iterate over each list item to extract the name and percentage
    output_list[1] = [None]*len(output_list[0])
    print(len(li_elements))
    for li in li_elements:
        # Extract the name from the <dt> element
        name = get_element_by(li, By.TAG_NAME, "dt").text
        
        # Extract the percentage from the <span class="usagerate_play_rate__aChNq"> element
        percentage = get_element_by(li, By.CLASS_NAME, "usagerate_play_rate__aChNq").text
        # if not name or not percentage: continue
        assert name in name_indices.keys()
        index = name_indices[name]
        print(f"Name: {name}, Percentage: {percentage}")
        output_list[1][index] = str(round(float(percentage)/100, 5))
    assert len(output_list[0]) == len(output_list[1])
    # Close the browser
    driver.quit()
    
    with open("winrates.csv", "w") as file:
        for line_list in output_list:
            print(line_list)
            line = ','.join(line_list)
            
            file.write(line)
            file.write('\n')

if __name__ == "__main__":
    main()