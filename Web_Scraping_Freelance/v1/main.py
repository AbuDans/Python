from extract_results import get_logged_in,start_search,threaded_get_url_emails
import threading
import queue



        

            
def main():
    session=get_logged_in("config.json")
    # Use the session to access the protected page
    full_urlar=start_search(session)
    q = queue.Queue()
    lock = threading.Lock()
    threads = []
    
    # Put URLs into the queue
    for url in full_urlar:
        q.put(url)
    # Start threads if not already started
    if not threads:
        for _ in range(5):  # Adjust the number of threads as needed
            t = threading.Thread(target=threaded_get_url_emails, args=(session, q, lock, "email.txt"))
            t.start()
            threads.append(t)
    # Signal threads to terminate
    for _ in threads:
        q.put(None)
    # Wait for all threads to complete
    for t in threads:
        t.join()        

   






if __name__ == '__main__':
    main()








