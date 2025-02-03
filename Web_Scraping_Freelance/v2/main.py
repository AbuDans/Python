from extract_results import get_logged_in_session,start_search,extract_email_from_page,create_search_url,get_search_page_results
from utils import load_configs
import threading
import queue

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
def process_pages(search_info):
    ar_links=[]
    offset=0
    q = queue.Queue()
    lock = threading.Lock()
    threads = []
    while(search_info['total_pages']>0):
        search_url=create_search_url(search_info['search_query'],offset)
        ar_links=get_search_page_results(search_info['session'] , search_url,"links.txt")
        search_info['total_pages']-=1
        print(len(ar_links))
        offset+=15
         #Put URLs into the queue
        for url in ar_links:
            q.put(url)
        # Start threads if not already started
        if not threads:
            for _ in range(5):  # Adjust the number of threads as needed
                t = threading.Thread(target=threaded_get_url_emails, args=(search_info['session'], q, lock, "email.txt"))
                t.start()
                threads.append(t)
        # Signal threads to terminate
    for _ in threads:
        q.put(None)
        # Wait for all threads to complete
    for t in threads:
        t.join()
        ar_links=[]            

def main():
    configs = load_configs('config.json')
    session=get_logged_in_session(email=configs['email'], password=configs['password'])
    # Use the session to access the protected page
    search_info=start_search(session,search_segments=configs['search_segments'])
    process_pages(search_info)     

if __name__ == '__main__':
    main()








