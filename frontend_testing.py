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
from selenium.webdriver.chrome.service import Service  #A Service class that is responsible for the starting and stopping of chromedriver.
from selenium.webdriver.chrome.options import Options # The objects let the web driver customize the behavior of a web browser as known as options. 
                                                      # Here, we have stated the ChromeOptions. You need to state the options of the browser in which you are running the script.
from time import sleep
import requests

# Webdriver: A set of methods that are used to control web browsers and interact with the elements on the web page.
# define the path where the browser driver is present. Here, we have used the Chrome Driver path,
# Then, we will initiate the chrome driver using the chrome driver path.

# WebDriver Path
path = "C:\\Users\\Smart\\Downloads\\chromedriver-win64\\chromedriver.exe"
service = Service(path)  #  define the path where the browser driver is present using the Service function. Here, we have used the Chrome Driver path.
chrome_options = Options() # Once we have stated the options, we can pass the arguments to options
chrome_options.add_experimental_option("detach",True) # tells ChromeDriver to keep the browser window open even after the WebDriver session is ended.

# Start WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

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
