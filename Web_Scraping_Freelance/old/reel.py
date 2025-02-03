import requests
import os
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the URLs
login_page_url = 'https://profile.w3schools.com/login'  # Replace with the actual login page URL
protected_url = 'https://profile.w3schools.com/plan-selection'  # Replace with the actual protected page URL

# Define login credentials
login_data = {
    'login': '',  # Replace with your actual username or email
    'password': ''  # Replace with your actual password
}

def login_and_save_cookies():
    # Create a session object
    session = requests.Session()

    # Fetch the login page
    response = session.get(login_page_url)

    # Check if the request was successful
    if response.ok:
        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')

        # Send a POST request to login
        response = session.post(login_page_url, data=login_data)

        # Check if the login was successful
        if response.ok:
            print('Login successful!')

            # Extract cookies
            cookies = session.cookies.get_dict()

            # Save cookies to a JSON file
            with open('cookies1.json', 'w') as f:
                json.dump(cookies, f)

            return session
        else:
            print('Login failed!')
            return None
    else:
        print('Failed to fetch the login page')
        return None

# Function to load cookies from a JSON file
def load_cookies(session):
    with open('cookies1.json', 'r') as f:
        cookies = json.load(f)
    session.cookies.update(cookies)

# Function to check if the session is still logged in
def is_logged_in(session):
    response = session.get(protected_url)
    return response.ok

# Main function
def main():
    session = requests.Session()

    # Check if cookies.json exists
    if os.path.exists('cookies1.json'):
        print('Loading cookies from cookies.json...')
        load_cookies(session)

        # Check if the session is still logged in
        if is_logged_in(session):
            print('Session is still logged in.')
        else:
            print('Session is not logged in. Re-logging in...')
            os.remove('cookies1.json')
            session = login_and_save_cookies()
    else:
        print('cookies1.json not found. Logging in...')
        session = login_and_save_cookies()

    # Use the session to access the protected page
    if session and is_logged_in(session):
        response = session.get(protected_url)
        if response.ok:
            print('Accessed protected page successfully!')
            print(response.text)  # Print the response content or process as needed
        else:
            print('Failed to access protected page')
            print('Status code:', response.status_code)
            print('Response:', response.text)

if __name__ == '__main__':
    main()
