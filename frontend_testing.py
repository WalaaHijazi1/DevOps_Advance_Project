"""
Frontend testing – for web interface testing (module name = frontend_testing.py):
1. Name the module frontend_testing.py
2. The script will:
 Start a Selenium Webdriver session.
 Navigate to web interface URL using an existing user id.
 Check that the user name element is showing (web element exists).
 Print user name (using locator).
"""


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import os
from time import sleep
import requests

# Specify the path to ChromeDriver
#service = Service('./chromedriver')
#service = Service('/usr/local/bin/chromedriver')

# Set Chrome options
#chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode
#chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
#chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage

# Create a unique user data directory
#user_data_dir = os.path.join(tempfile.mkdtemp(), 'chrome-profile')
#chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Start WebDriver
#driver = webdriver.Chrome(service=service, options=chrome_options)

driver_options = Options()

driver_options.add_argument("--headless=new")
driver_options.add_argument("--no-sandbox")
driver_options.add_argument("--disable-dev-shm-usage")
    
    
driver_options.add_argument(f"--user-data-dir={os.path.expanduser('~')}/chrome_data")
    
driver_options.add_argument("--remote-debugging-port=9222")  # Unique devtools port
    
# Set up the ChromeDriver Service
#service = Service(ChromeDriverManager().install())

# Set up the ChromeDriver Service
chromedriver_path = "/root/.wdm/drivers/chromedriver/linux64/134.0.6998.88/chromedriver-linux64/chromedriver"
service = Service(executable_path=chromedriver_path)

# Initialize the Chrome WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=driver_options)



# Define the URL to test
user_id = 1
#url = f"http://127.0.0.1:5000/users/{user_id}"
url = f"http://172.17.0.1:5000/users/{user_id}"


    
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

