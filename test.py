import requests
import sys
from requests.exceptions import MissingSchema
import numpy as np
from multiprocessing import Process
import time

def links_status_check(start_page, pages, requests):
    for page in pages:
        response = requests.get(start_page + '/' + page)
        if (response.status_code != 429):
            print(start_page + '/' + page, response.status_code)
        else:
            wait_seconds = int(response.headers['Retry-After'])
            print("Too many requests. Waiting for " + str(wait_seconds) + " seconds")

            time.sleep(wait_seconds)

            response = requests.get(start_page + '/' + page)
            print(start_page + '/' + page, response.status_code)


    return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python3 test.py https://url_example.exm path_to_file")
        exit(1)
    start_page = sys.argv[1]

    NUMBER_OF_PROCESS = 10

    try:
        file = open(sys.argv[2], 'r')
        pages = []
        for line in file:
            pages.append(line[:-1])
        pages = np.array(pages)

        seg = len(pages) // NUMBER_OF_PROCESS
        for i in range(NUMBER_OF_PROCESS):
            seg_end = seg * (i + 1) if ((seg * (i + 1)) < len(pages)) else (len(pages) - 1)
            proc = Process(target = links_status_check, args=(start_page, pages[(seg * i) : (seg_end)], requests))
            proc.start()

        file.close()

    except FileNotFoundError:
        print("Incorrect path to file " + sys.argv[2])
    except MissingSchema:
        print('URL must be full. For example: https://github.com')