import requests
from bs4 import BeautifulSoup
import re 
import threading
import queue








def extract_emails_from_url(session, q, lock, output_file='emails.txt'):
    while True:
        url = q.get()
        if url is None:  
            break

        try:
            response = session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').text.strip() if soup.find('title') else "No Title Found"
            td_tags = soup.find_all('td')
            email_regex = r'[\w\.-]+@[\w\.-]+\.[\w]{2,6}'
            emails = []
            for td_tag in td_tags:
                text = td_tag.text.strip()
                match = re.search(email_regex, text)
                if match:
                    email = match.group(0)
                    emails.append(f"{title}: {email}")
            if not emails:
                emails.append(f"{title}: not found")        
        
            # Writing to file using thread lock
            with lock:
                with open(output_file, 'a') as file:
                    for email in emails:
                        file.write(f"{email}\n")
                        print(f"Email extracted and written to file: {email}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
        finally:
            q.task_done()

def fetch_all_results(html_content, api_url, session, output_file):
    line_number = 1
    initial_results = extract_total_results(html_content, 1)
    total_results = extract_total_results(html_content)
    print(f"Total Results: {total_results}")
    if initial_results is None or total_results is None:
        print("Unable to fetch initial or total results. Exiting.")
        return

    q = queue.Queue()
    lock = threading.Lock()
    threads = []

    try:
        with open(output_file, 'a') as file:
            offset = 0
            while offset < total_results:
                # Construct the URL with or without the offset parameter
                request_url = api_url if offset == 0 else f"{api_url}&offset={offset}"
                response = session.get(request_url)
                #print(response.text)
                if response.ok:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title_links = soup.find_all('a', class_='title')
                    #print(title_links)
                    full_urlar = []
                    for link in title_links:
                        if line_number > total_results:
                            break
                        href = link.get('href')
                        full_url = f"https://www.northdata.com/{href}"
                        file.write(full_url + '\n')
                        line_number += 1
                        #print(full_url)
                        full_urlar.append(full_url)
                    
                    for url in full_urlar:
                        q.put(url)

                    # Start threads if not already started
                    if not threads:
                        for _ in range(5):  # Adjust the number of threads as needed
                            t = threading.Thread(target=extract_emails_from_url, args=(session, q, lock, "email.txt"))
                            t.start()
                            threads.append(t)

                    if (total_results - initial_results) < 15:
                        initial_results += (total_results - initial_results)
                    else:
                        initial_results += 15
                    offset += 15

                    if len(title_links) < 15:
                        break
                else:
                    print(f"Request failed. Status code: {response.status_code}")
                    break

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    finally:
        # Add sentinel values to stop the threads
        for _ in threads:
            q.put(None)

        # Wait for all threads to complete
        for t in threads:
            t.join()




def extract_and_save_title_links(html_content,session,url, output_file='title_links.txt'):
    api_url=url
    fetch_all_results(html_content,api_url,session,output_file)




   