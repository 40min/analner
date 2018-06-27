import urllib3
from datetime import datetime
from hashlib import md5

import certifi
from bs4 import BeautifulSoup


grabbed_headers_path = './grabbed_headers'

target_base = 'https://www.onliner.by/'

cookies = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/61.0.3163.100 Safari/537.36',
    'Cookie':  ''
}


def request_page(url):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', url, headers=headers)
    if r.status != 200:
        raise Exception(f"Page {url} is unaccessible")
    return r.data


def get_current_date_file_name():
    ts = datetime.now().strftime("%y-%m-%d")
    return f"{grabbed_headers_path}/{ts}.txt"


def get_header_hash(header):
    return md5(header.encode('utf-8'))


def save_data(file_name, headers_list):
    data_hashes = []
    with open(file_name, 'a+') as f:
        f.seek(0)
        data = f.read()
        if data:
            data_hashes = list(
                map(
                    lambda d: get_header_hash(d),
                    data.split("\n")
                )
            )

        # stopping here on bug
        for h in headers_list:
            if get_header_hash(h) not in data_hashes:
                f.write(f'{h}\n')


def fetch_fresh_headers(current_file_name):
    page = request_page(target_base)
    soup = BeautifulSoup(page, 'html5lib')
    headers_list_mobile = list(
        map(
            lambda a: a.string,
            soup.find_all('span', {'class': 'helpers_show_mobile-small'})
        )
    )
    headers_list = list(
        map(
            lambda a: a.find('span', {'class': 'text-i'}).string,
            soup.find_all('a', {'class': 'b-teasers-2__teaser-i'})
        )
    )
    headers_list_full = headers_list + headers_list_mobile

    print(f'found {len(headers_list_full)}:')

    return headers_list_full


if __name__ == "__main__":
    current_fn = get_current_date_file_name()
    headers_list = fetch_fresh_headers(current_fn)
    save_data(current_fn, headers_list)
