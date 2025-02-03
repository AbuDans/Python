import re
import os
import json
import math
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from utils import get_segment_list
from lxml import etree
class NotLoggedInException(Exception):
    pass

#  load cookies from a JSON file
def load_cookies(session):
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
    session.cookies.update(cookies)
    return session

#  check if the session is still logged in
def is_logged_in(session):
    response = session.get('https://www.northdata.com/_selfcare')
    return response.ok

def login_and_save_cookies(email, password):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0'
    }
    # Update session headers
    session.headers.update(headers)

    # Fetch the login page with updated headers
    login_url = 'https://www.northdata.com/rpc.json/user/login'
    session.get(login_url)

    # Send a POST request to login with updated headers
    payload = {
        'email' : email,
        'password' : password,
        'token' : ''
    }
    response = session.post(login_url, data=payload)

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

def get_logged_in_session(email=None, password=None):
    session = requests.Session()
    if os.path.exists('cookies.json'):
        print('Loading cookies from cookies.json...')
        session = load_cookies(session)
        # Check if the session is still logged in
        if is_logged_in(session):
            print('Session is still logged in.')
            return session
        else:
            print('Session is not logged in. Re-logging in...')
            os.remove('cookies.json')
            session = login_and_save_cookies(email, password)
            return session
    else:
        print('cookies.json not found. Logging in...')
        session = login_and_save_cookies(email, password)
        return session

def start_search(session : requests.Session,search_segments=None):
    if not is_logged_in(session):
        raise NotLoggedInException
    response = session.get('https://www.northdata.com/_selfcare')
    if response.ok:
        print("Search is being performed.")
        segmentcodes=get_segment_list()
        offset=0
        search_query=create_search_query(session,segmentcodes,search_segments)
        search_url=create_search_url(search_query,offset)
        total_results=get_total_results(session,search_url)
        total_pages=get_total_pages(total_results)
        search_info={
            'session':session,
    'search_query': search_query,
    'search_url': search_url,
    'total_results': total_results,
    'total_pages': total_pages
        }
        return search_info
    else:
        print('Failed to access protected page')


def create_search_query(session, segment_codes,search_segments):
    try:
        query_params = {}
        for i, param in enumerate(search_segments):
            if param.startswith('segmentCodes='):
                search_segments[i] = f'segmentCodes={segment_codes}'
                break 
        print(search_segments)    
        for segment in search_segments:
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
        return query_params
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")

def get_total_pages(total_results):
    return math.ceil(total_results/15)

def get_total_results(session,search_url):
    response = session.get(search_url)
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        p_elements = soup.find_all('p')
        if len(p_elements) >= 2:
            p = p_elements[1]
            text = p.get_text(strip=True)
            total_results = float(re.search(r'\d+', p.get_text().strip().split('results of ')[1].split(' total.')[
                0].strip().replace(',', '')).group())
            print(total_results)
            return min(total_results,120)

    except Exception as e:
        print(f"Error extracting total results: {e}")
    return None    



def create_search_url(search_query,offset):
    base_url = 'https://www.northdata.com/'
    url = base_url + '?' + urlencode(search_query)
    if offset>0:
        url = f"{url}&offset={offset}"
    return url

def get_search_page_results( session ,search_url,output_file):
    try:
        with open(output_file, 'a') as file:
            offset = 0
         # Construct the URL with or without the offset parameter
            response = session.get(search_url)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                xpath_expression = "//div[@class='column']/div[@class='ui feed']/div[@class='event']//a"

# Use lxml for robust XPath support
                title_links = []
                try:
                   
                    xml_content = etree.fromstring(str(soup))  # Convert to lxml element tree
                    title_links = xml_content.xpath(xpath_expression)
                except ImportError:
                # Fallback to BeautifulSoup's find_all for basic functionality
                    for event in soup.find_all('div', class_='event'):
                        for potential_link in event.find_all('a'):
                            title_links.append(potential_link)
                urlar = []
                for link in title_links:
                    href = link.get('href')
                    full_url = f"https://www.northdata.com/{href}"
                    file.write(f"{full_url}\n")
                    urlar.append(full_url)    
                return urlar                    
            else:
                print(f"Request failed. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")








def extract_email_from_page(url, session, output_file='emails.txt', lock=None):
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
                # print(f"Email extracted from {url}: {email} (Title: {title})")
                return

        with lock:
            file.write(f"{title}: Not Found\n")
        # print(f"No email found on {url} (Title: {title})")
