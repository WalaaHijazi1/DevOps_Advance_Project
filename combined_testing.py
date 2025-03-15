"""
Combined testing – for Web interface, REST API and Database testing
(module name = combined_testing.py):
The script will:
 Post any new user data to the REST API using POST method.
 Submit a GET request to make sure data equals to the posted data.
 Using pymysql, check posted data was stored inside DB (users table).
 Start a Selenium Webdriver session.
 Navigate to web interface URL using the new user id.
 Check that the user name is correct.

Any failure will throw an exception using the following code: raise Exception("test failed")
"""


import requests
import datetime
import pyodbc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "http://127.0.0.1:5000/users"

# the post function is explained in the backend testing, this one is not very different from the one in the backend test.
# if you want to understand the steps in here please go back to the function in the backend testing file.
def post_new_user():

    global new_user_data

    new_user_data = {
        "user_name" : "freda",
        "creation_date" : datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")
    }

    response = requests.post(url, json=new_user_data)
    
    if response.status_code == 200:
        print("POST request passed successfully, the response is:", response.json())
    else:
        raise Exception(f"API POST request failed. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json() 


# same here the get_requst is very similar to the function in the backend_testing so, thier it was explained explicitly.
def get_request():
    global new_user_data

    new_user_id = check_data()
    get_response = requests.get(f"{url}/{new_user_id}", json = new_user_data)

    data_response = get_response.json()  # Convert response to a dictionary
    new_user_name = new_user_data["user_name"]
    assert data_response["user_name"] == new_user_name, \
    f"Unexpected user name, data from get response: {data_response}. {data_response.get('user_name')}"


    return print(f"get response was successfully done with data : {get_response.json()}")


# in the db_connector file, the connection process to the table data base was explained on how and why.
def check_data():

    global new_user_data

    # connect to the sql table in Azure:
    # connection details:
    server = "tcp:usersdbserver.database.windows.net,1433"
    database = "users_data"
    username = "adminwalaa"  # Your Azure AD login
    password = "Walaa2511"  

    # ODBC connection string:
    connection_str = f"""
                Driver={{ODBC Driver 18 for SQL Server}};
                Server={server};
                Database={database};
                Uid={username};
                Pwd={password};Encrypt=yes;
                TrustServerCertificate=no;
                Connection Timeout=30;
                    """
    try:
        conn = pyodbc.connect(connection_str)
        cursor = conn.cursor()
        cursor.execute("SELECT DB_NAME()")
        db_name = cursor.fetchone()[0]
        print(f"Connected successfully! {db_name}")

        user_name = new_user_data["user_name"]
        print(f"user name is {user_name}")



        # fetching user id of the giving user name:
        cursor.execute("SELECT users_id FROM dbo.users WHERE user_name= ?",(new_user_data["user_name"],))
        user_id = cursor.fetchone()[0]
        conn.close()
        
        print(f"You have successfully connected to the data base, the data that was fetched is: {user_id} for {user_name}")

        print(f"user id is: {user_id}, type of user id is {type(user_id)}")

        return user_id
       
    # if the connection failed through the process an error will be raised:
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def selenium_session():

    global new_user_data
    # retraiting the user name from data that I defined in the beginning
    user_name = new_user_data["user_name"]
    # using the function that we wrote before to get the user id which appropriate for the user name
    # in the new_user_data , it's a global variable and it is defined in the check_data func.
    new_user_id = check_data()

    options = Options() # An Options object is created to customize Chrome’s behavior.this will leave the browser open even after everything is completed
    options.add_experimental_option("detach",True) # instructs ChromeDriver to keep the browser window open even after the WebDriver session ends. This is useful for debugging.
    path = r"C:\Users\Smart\Downloads\chromedriver-win64\chromedriver.exe" # path to Chrome Driver.
    service = Service(path) # A Service is created with the given path, and then the Chrome WebDriver is started with the specified options and service.
    driver = webdriver.Chrome(service=service, options = options)


    new_url = f"http://127.0.0.1:5000/users/{new_user_id}"

    driver.get(new_url) # The driver navigates to the constructed URL.
    time.sleep(2) # A short sleep of 2 seconds is introduced to allow the page time to load completely before further actions are taken.

    wait = WebDriverWait(driver, 10) # A WebDriverWait object is created with a maximum wait time of 10 seconds. This will be used to pause execution until certain elements appear on the page.

    try:
        # The code waits until an element with the HTML attribute id="user" appears on the page. This element is expected to contain the displayed user name.
        element = wait.until(EC.presence_of_element_located((By.ID, "user")))  # For valid user/ EC - Explicit Wait!
        
        # Once the element is found, its text content is extracted and stored in displayed_name.
        displayed_name = element.text
        # The function prints the displayed name and checks whether it matches the expected user_name.
        print(f"Displayed Name: {displayed_name}")

        if displayed_name != user_name:
            raise Exception(f"Displayed name mismatch: Expected {user_name}, but got {displayed_name}")
        
    
    # If they do not match, an exception is raised with a descriptive error message.
    except Exception as e:
        # If the user doesn't exist, the error message will be shown
        element = wait.until(EC.presence_of_element_located((By.ID, "error")))  # For error message
        error_message = element.text
        print(f"Error: {error_message}")
        raise Exception(f"Test failed: {error_message}")
    
    # Regardless of whether the try block succeeds or an exception is raised, the finally block ensures that the browser is properly closed.
    # driver.close() closes the current window, and driver.quit() ends the WebDriver session.
    finally:
        driver.close()
        driver.quit()



# Run all functions in sequence
def main():
    post_new_user()
    time.sleep(1)  # Give time for API processing
    get_request()
    time.sleep(1)
    check_data()
    time.sleep(1)
    selenium_session()

if __name__ == "__main__":
    main()