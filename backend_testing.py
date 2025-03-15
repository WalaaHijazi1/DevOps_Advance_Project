"""
Backend testing – for REST API and Database testing (module name = backend_testing.py):
1. Name the module backend_testing.py
2. The script will:
 Post a new user data to the REST API using POST method.
 Submit a GET request to make sure status code is 200 and data equals to the
posted data.
 Check posted data was stored inside DB (users table).
Example:
Step 1: POST the below (marked) JSON payload to 127.0.0.1:5000/users/1
{“user_name”: “john”}
Step 2: Call 127.0.0.1:5000/users/1 using GET method and make sure the user_name
“john” returned in the response and response code is 200.
Step 3: Query (using pymysql) users table and make sure “john” is stored under id 1
"""

import requests
import datetime


url = 'http://127.0.0.1:5000/users'

# Post a new user data to the REST API using POST method.
def post_new_data():

    global new_data
    # data that I want to insert to sql table,
    # it has user id, user name and creation date.
    # Sending an HTTP POST request using the requests library in Python.
    # using a specific url, which contains the end point that I want to send to it the new_data.
    # the line 'json=new_data' automatically turns new_data into json format.
    # the assertion statement, which is used to verify whether a certain condition is True. 
    # If the condition is False, it raises an AssertionError with a specified message.
    # response.status_code == 200 checks whether the HTTP status code of the response is 200, which indicates success (OK) in HTTP.
    # I can delete it because in the app python file there is already have a return status code if there is a problem, but the error raising message
    # can help detect the exact error and handled in a short time.
    new_data = {'user_id' : 33,
                'user_name': 'jhon', 
                'creation_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
    

    response = requests.post(f"{url}" , json= new_data) # here It sends an HTTP POST request using the requests.post() method from the Requests library.
    # json = new_data convert the python dictionary into json string, and Set the Content-Type header of the request to application/json.
    # The response variable stores the Response object returned by requests.post(). This object includes: 
    # 1) The HTTP status code. 2) Response headers. 3) The content/body of the response, which you can access with methods like .json().
    data_from_post = response.json() # accessing the response data with json method
    # checking the status code of the response if the test was passed successfull, if not it raises an error!
    assert response.status_code == 200 , f"API Error! Status Code: {response.status_code}, Response: {response.text}"
    return print(f"get test was successfully passed. data from get response: {data_from_post}")


def get_endpoint():
    global new_data
    user_id = new_data['user_id']
    get_response = requests.get(f"{url}/{user_id}", json = new_data) # sends an HTTP GET request to the constructed URL. GET requests are typically used to retrieve data from a server.
    # The parameter json=new_data is intended to serialize the Python dictionary new_data into JSON format and include it in the request body.

    data_response = get_response.json() # convert the Response object to a JSON dictionary using its .json() method, then access the key
    # data_response: is a Response object that contains details like the status code, headers, and body of the HTTP response from the server.

    # checking if the user name in the retrieved data is mike the name that was put by the put request earlier. if not it raises an error!.
    assert data_response.get("user_name") == "mike" , f"Unexpected user name, data from get response: {data_response}. {data_response.get("user_name")}"
    return print(f"GET test passed successfully! Data from GET response: {data_response}")



post_new_data()
get_endpoint()



