import time
import threading
import queue

from extract_results import get_logged_in_session, start_search, extract_email_from_page, create_search_url, \
    get_search_page_results
from utils import load_configs,save_progress,load_progress


def threaded_get_url_emails(session, urls_queue, lock, output_file):
    while not urls_queue.empty():
        url = urls_queue.get()
        while 1:
            try:
                extract_email_from_page(url, session, output_file, lock)
                break
            except Exception as e:
                time.sleep(1)
                print(f"Error processing {url}: {e}")
        urls_queue.task_done()

def process_pages(search_info):
    q = queue.Queue()
    lock = threading.Lock()
    last_page = load_progress(search_info['segment_codes'])
    for i in range(last_page, search_info['total_pages']):
        offset = i*15

        while 1:
            try:
                search_url = create_search_url(search_info['search_query'], offset)
                ar_links = get_search_page_results(search_info['session'], search_url, "links.txt")
                save_progress(i,search_info['segment_codes'])
                break
            except Exception as e:
                print(e)
                time.sleep(3)

        # Put URLs into the queue
        for url in ar_links:
            q.put(url)
        threads = []

        # TODO: make this number of threads be a dynamic input
        for _ in range(5):
            t = threading.Thread(target=threaded_get_url_emails,args=(search_info['session'], q, lock, "email.txt"))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

def main():
    configs = load_configs('config.json')
    session = get_logged_in_session(email=configs['email'], password=configs['password'])
    search_info = start_search(session, search_segments=configs['search_segments'])
    process_pages(search_info)


if __name__ == '__main__':
    main()
