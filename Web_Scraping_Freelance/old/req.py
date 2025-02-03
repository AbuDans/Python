import requests
from bs4 import BeautifulSoup
import json


# https://www.northdata.com/rpc.json/user/login  POST



#Create a session object
session = requests.Session()

# Send a POST request to login
login_url = 'https://profile.w3schools.com/login'  # Replace with the actual login URL
login_data = {
    'login': '',  # Replace with the actual form field names and values
    'password': ''
}

response = session.post(login_url, data=login_data)

# Check if the login was successful and save cookies to a JSON file
if response.ok:
    print('Login successful!')

    # Extract cookies
    cookies = session.cookies.get_dict()
    print('Cookies:', cookies)

    # Save cookies to a JSON file
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)
else:
    print('Login failed!')

#Load cookies from JSON file
with open('cookies.json', 'r') as f:
    cookies = json.load(f)

# Use cookies in subsequent requests
protected_url = 'https://profile.w3schools.com/plan-selection'  # Replace with the actual URL
response = session.get(protected_url, cookies=cookies)

if response.ok:
    print('Accessed protected page!')
    print(response.text)  # Or process the response as needed
else:
    print('Failed to access protected page!')




# Define the URL of the protected page
protected_url = 'https://profile.w3schools.com/plan-selection'  # Replace with the actual protected page URL

# Load cookies from the JSON file
with open('cookies.json', 'r') as f:
    cookies = json.load(f)

# Create a session object
session = requests.Session()

# Update the session's cookies
session.cookies.update(cookies)

# Use the session to access the protected page
response = session.get(protected_url)

# Check if the access was successful
if response.ok:
    print('Accessed protected page successfully!')
    print(response.text)  # Print the response content or process as needed
else:
    print('Failed to access protected page')
    print('Status code:', response.status_code)
    print('Response:', response.text)
