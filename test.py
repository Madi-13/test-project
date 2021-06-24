import requests
import sys
from requests.exceptions import MissingSchema

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python3 test.py start_https://url_example.exm path_to_file")
        exit(1)
    start_page = sys.argv[1]

    try:
        file = open(sys.argv[2], 'r')

        for line in file:
            page = start_page + "/" + line[:-1]
            response = requests.get(page)
            print(page, response.status_code)
        file.close()

    except FileNotFoundError:
        print("Incorrect path to file " + sys.argv[2])
    except MissingSchema:
        print('URL must be full. For example: https://github.com')