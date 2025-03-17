"""
"""
#Frontend testing – for web interface testing (module name = frontend_testing.py):
#1. Name the module frontend_testing.py
#2. The script will:
# Start a Selenium Webdriver session.
# Navigate to web interface URL using an existing user id.
# Check that the user name element is showing (web element exists).
# Print user name (using locator).
"""
"""
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service  #A Service class that is responsible for the starting and stopping of chromedriver.
from selenium.webdriver.chrome.options import Options # The objects let the web driver customize the behavior of a web browser as known as options. 
                                                      # Here, we have stated the ChromeOptions. You need to state the options of the browser in which you are running the script.
from time import sleep
import requests
import tempfile
import os
import sys

import chromedriver_autoinstaller



# Redirect stderr to /dev/null to suppress X11 warnings
sys.stderr = open(os.devnull, 'w')


# Webdriver: A set of methods that are used to control web browsers and interact with the elements on the web page.
# define the path where the browser driver is present. Here, we have used the Chrome Driver path,
# Then, we will initiate the chrome driver using the chrome driver path.


# Automatically download and install chromedriver if not present
chromedriver_autoinstaller.install()

# Specify the path to the ChromeDriver
service = Service('/usr/local/bin/chromedriver')

# Create a unique user data directory
user_data_dir = os.path.join(tempfile.mkdtemp(), 'chrome-profile')
# Create a unique user data directory
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Set the path to chromedriver within the virtual environment
#chromedriver_path = os.path.join(os.environ['VIRTUAL_ENV'], 'bin', 'chromedriver')
#service = Service(chromedriver_path)


# WebDriver Path
# path = "C:\\Users\\Smart\\Downloads\\chromedriver-win64\\chromedriver.exe"
# service = Service(path)  #  define the path where the browser driver is present using the Service function. Here, we have used the Chrome Driver path.

chrome_options = Options() # Once we have stated the options, we can pass the arguments to options



chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Create a unique user data directory
user_data_dir = os.path.join(tempfile.mkdtemp(), 'chrome-profile')
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Initialize WebDriver with ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


#chrome_options.add_experimental_option("detach",True) # tells ChromeDriver to keep the browser window open even after the WebDriver session is ended.

# Start WebDriver
#driver = webdriver.Chrome(service=service, options=chrome_options)

user_id = 1
url = f"http://127.0.0.1:5000/users/{user_id}"

# check if URL Exists Before Opening
try:
    response = requests.get(url)   # uses the Requests library to send an HTTP GET request to the specified URL.
    # sending a request to the server endpoint uding the specified 'url'.
    if response.status_code != 200:   # Status Code: Indicates whether the request was successful (200) or not.
        # here it will not return 200 because it access the if condition if there was an error in the process.
        print(f"Error: URL {url} returned {response.status_code}")
        driver.quit()
        exit()

    print(f"URL {url} is reachable, launching browser...")

# if the connection to the driver did not work, an error will be raised, and then quit:
except requests.RequestException as e:
    print(f"Connection error: {e}")
    driver.quit()
    exit()

# Navigate to the Web Interface
driver.get(url)

# Wait for page to load
sleep(2)

# Close Browser
driver.quit()
"""


"""
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Create a unique user data directory
user_data_dir = os.path.join(tempfile.mkdtemp(), 'chrome-profile')
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Initialize WebDriver with ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

user_id = 1
url = f"http://127.0.0.1:5000/users/{user_id}"

# Navigate to the Web Interface
driver.get(url)

try:
    # Wait for the user name element to be present
    user_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user_name'))
    )
    # Print the user name
    print(user_name_element.text)
except TimeoutException:
    print("Timed out waiting for user name element to load.")
finally:
    # Close the browser
    driver.quit()
"""



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Import expected_conditions

import tempfile
import os
import time
from time import sleep
import requests

# Specify the path to ChromeDriver
service = Service('./chromedriver')

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage

# Create a unique user data directory
user_data_dir = os.path.join(tempfile.mkdtemp(), 'chrome-profile')
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Start WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the URL to test
user_id = 1
url = f"http://127.0.0.1:5000/users/{user_id}"


    
try:
    response = requests.get(url)   # uses the Requests library to send an HTTP GET request to the specified URL.
    # sending a request to the server endpoint uding the specified 'url'.
    if response.status_code != 200:   # Status Code: Indicates whether the request was successful (200) or not.
        # here it will not return 200 because it access the if condition if there was an error in the process.
        print(f"Error: URL {url} returned {response.status_code}")
        driver.quit()
        exit()

    print(f"URL {url} is reachable, launching browser...")

# if the connection to the driver did not work, an error will be raised, and then quit:
except requests.RequestException as e:
    print(f"Connection error: {e}")
    driver.quit()
    exit()

# Navigate to the Web Interface
driver.get(url)

# Wait for page to load
sleep(2)

# Close Browser
driver.quit()

"""

# Check if the URL is reachable
try:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: URL {url} returned {response.status_code}")
        driver.quit()
        exit()
    print(f"URL {url} is reachable, launching browser...")
except requests.RequestException as e:
    print(f"Connection error: {e}")
    driver.quit()
    exit()
    


# Navigate to the URL
driver.get(url)

# Wait for the page to load
time.sleep(2)  # Adjust the sleep time as needed


# Wait for the username element to appear
try:
    username_locator = (By.ID, "username")  # Update this to the correct locator
    username_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(username_locator)
    )
    print(f"Username: {username_element.text}")
except Exception as e:
    print(f"Error: Could not find the username element. {e}")


# Check if the username element exists
#try:
    # Locate the username element (replace 'username_locator' with the actual locator)
    #username_locator = (By.ID, "user_name")  # Example: Using ID as the locator
   # username_element = driver.find_element(*username_locator)

    # Print the username
    #print(f"Username: {username_element.text}")
#except Exception as e:
 #   print(f"Error: Could not find the username element. {e}")

# Close the browser
driver.quit()
"""