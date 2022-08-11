from bs4 import BeautifulSoup
import requests
import time
from os import path
from requests.auth import HTTPBasicAuth


LOG_INTERVAL = 120  # in seconds
OUTPUT_FILE = 'output.csv'
URL = 'http://10.10.46.149/status.html'


def main():
    if not path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'w') as f:
            f.write('time,current_power,total_power\n')


    while True:
        try:
            current_power, total_power = retrieve_infos()
        except ValueError:
            print('Error while retrieving infos')
            continue

        print(f'Current power: {current_power}W, Total power: {total_power}W')

        with open(OUTPUT_FILE, 'a') as f:
            f.write(f'{time.time()},{current_power},{total_power}\n')

        time.sleep(LOG_INTERVAL)


def retrieve_infos():
    response = requests.get(URL)

    if response.status_code == 401:
        response = requests.get(URL, auth=HTTPBasicAuth('admin', 'admin'))

    soup = BeautifulSoup(response.content, 'html.parser')
    page_js = soup.head.findAll(type="text/javascript")[1]
    page_js_vars = page_js.text.split('\n')
    interesting_infos = page_js_vars[6:9]
    current_power, _, total_power = [float(e.split('"')[1]) for e in interesting_infos]

    return current_power, total_power


if __name__ == '__main__':
    main()
