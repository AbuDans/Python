import requests
from bs4 import BeautifulSoup
import re 
import threading
import queue
import requests
import os
import json
from urllib.parse import urlencode
from makejson import extract_login_data_from_json,extract_login_url_from_json,extract_protected_url_from_json,get_segment_list

def get_logged_in(configpath):
    login_data = extract_login_data_from_json(configpath)
    login_url = extract_login_url_from_json(configpath)
    protected_url = extract_protected_url_from_json(configpath)
    session = requests.Session()
    if os.path.exists('cookies.json'):
        print('Loading cookies from cookies.json...')
        session=load_cookies(session)
        # Check if the session is still logged in
        if is_logged_in(session,protected_url):
            print('Session is still logged in.')
            return session
        else:
            print('Session is not logged in. Re-logging in...')
            os.remove('cookies.json')
            session = login_and_save_cookies(login_data,login_url)
            return session
    else:
        print('cookies.json not found. Logging in...')
        session = login_and_save_cookies(login_data,login_url)
        return session

def login_and_save_cookies(login_data,login_url):
    session = requests.Session()
    headers = {
'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0'
}
    # Update session headers
    session.headers.update(headers)

    # Fetch the login page with updated headers
    response = session.get(login_url)

    # Send a POST request to login with updated headers
    response = session.post(login_url, data=login_data)

    if response.ok:
        print('Login successful!')
            # Here you can further process the login response if needed
        cookies = session.cookies.get_dict()

            # Save cookies to a JSON file
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)
            return session
    else:
        print('Login failed!')
        return None


#  load cookies from a JSON file
def load_cookies(session):
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
    session.cookies.update(cookies)
    return session

#  check if the session is still logged in
def is_logged_in(session,protected_url):
    response = session.get(protected_url)
    return response.ok



def start_search(session):
    protected_url = extract_protected_url_from_json("config.json")
    if session and is_logged_in(session,protected_url):
        response = session.get(protected_url)
        if response.ok:
            print("Search is being performed.")
            return perform_search_with_config(session,"config.json")
        else:
            print('Failed to access protected page')







def perform_search_with_config(session,config):
    try:
        base_url = 'https://www.northdata.com/'
         # Load configuration from JSON file
       
        get_segment_list()
        with open(config, 'r') as f:
            config = json.load(f)
        query_params = {}

# Assuming 'search_segments' is a list of segments from your JSON config
        for segment in config['search_segments']:
            if '=' in segment:
                key, value = segment.split('=')
                if key == 'segmentCodes' and '[' in value and ']' in value:
            # Extract segment codes from the value and format them correctly
                    segment_codes = value.strip('[]').split('|')
            # Ensure specific order if needed (e.g., 01.1 should come before 01)
                    segment_codes.sort(reverse=True)  # Sort in reverse order for your case
                    query_params[key] = segment_codes
                else:
                     query_params[key] = value
        
        # Construct full URL with query parameters
        url = base_url + '?' + urlencode(query_params)
         # Construct full URL with query parameters
        print("Search URL:")
        print(url)
        #Send GET request
        response = session.get(url)

        #Check if the request was successful
        if response.ok:
            return fetch_all_links(response.text,url,session,"links.txt")
        else:
            print(f"Request failed. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")






def fetch_all_links(html_content, api_url, session, output_file):
    line_number = 1
    initial_results = extract_total_results(html_content, 1)
    #total_results = extract_total_results(html_content)
    total_results = min(extract_total_results(html_content),143)
    print(f"Initial Results: {initial_results}")
    print(f"Total Results: {total_results}")
    if initial_results is None or total_results is None:
         print("Unable to fetch initial or total results. Exiting.")
         return
    try:
        with open(output_file, 'a') as file:
            offset = 0
            full_urlar = []
            while offset < total_results:
                # Construct the URL with or without the offset parameter
                request_url = api_url if offset == 0 else f"{api_url}&offset={offset}"
                response = session.get(request_url)
                #print(response.text)
                if response.ok:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title_links = soup.find_all('a', class_='title')
                    #print(title_links)
                    temp_urlar = []
                    for link in title_links:
                        if line_number > total_results:
                            break
                        href = link.get('href')
                        full_url = f"https://www.northdata.com/{href}"
                        file.write(f"{str(line_number)}: {full_url}\n")
                        line_number += 1
                        temp_urlar.append(full_url)
                        full_urlar.append(full_url)

                    if (total_results - initial_results) < 15:
                        initial_results += (total_results - initial_results)
                    else:
                        initial_results += 15
                    offset += 15
                else:
                    print(f"Request failed. Status code: {response.status_code}")
                    break      
        return full_urlar
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")



def extract_total_results(html_content,case=0):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        p_elements = soup.find_all('p')
        if len(p_elements) >= 2:  
            p = p_elements[1]  
            text = p.get_text(strip=True)
            if case == 1:
                initial_results = float(re.search(r'\d+', text.split('results of')[0].strip().replace(',', '')).group())
                return initial_results
            else:    
                total_results = float(re.search(r'\d+', p.get_text().strip().split('results of ')[1].split(' total.')[0].strip().replace(',', '')).group())
                return total_results

    except Exception as e:
        print(f"Error extracting total results: {e}")

    return None







def threaded_get_url_emails(session, queue, lock, output_file):
    while True:
        url = queue.get()
        if url is None:
            queue.task_done()
            break
        try:
            extract_email_from_page(url, session, output_file, lock)
        except Exception as e:
            print(f"Error processing {url}: {e}")
        finally:
            queue.task_done()

def extract_email_from_page(url, session, output_file='emails.txt', lock=None):
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip() if soup.find('title') else "No Title Found"

        td_tags = soup.find_all('td')

        email_regex = r'[\w\.-]+@[\w\.-]+\.[\w]{2,6}'
        with open(output_file, 'a') as file:
            for td_tag in td_tags:
                text = td_tag.text.strip()
                match = re.search(email_regex, text)
                if match:
                    email = match.group(0)
                    with lock:
                        file.write(f"{title}: {email}\n")
                    #print(f"Email extracted from {url}: {email} (Title: {title})")
                    return

            with lock:
                file.write(f"{title}: Not Found\n")
            #print(f"No email found on {url} (Title: {title})")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
