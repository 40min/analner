import os
import urllib3
import logging
from datetime import datetime
from hashlib import md5

import certifi
from bs4 import BeautifulSoup


TARGET_URL = 'https://www.onliner.by/'
COOKIES = {}
HEADERS_DEFAULT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/61.0.3163.100 Safari/537.36',
    'Cookie':  ''
}
MIN_PHRASE_WORDS = 7

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


def request_page(url):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', url, headers=HEADERS_DEFAULT)
    if r.status != 200:
        raise Exception("Page {} is unaccessible".format(url))
    return r.data


def get_header_hash(header):
    return md5(header.encode('utf-8')).hexdigest()


class HeadGrab:

    def __init__(self, data_path, target_url):
        self.data_path = data_path
        self.target_url = target_url

    def run(self):
        page = request_page(self.target_url)
        headers_list = self.fetch_page_headers(page)
        current_filename = self.get_current_date_file_name()
        self.save_data(current_filename, headers_list)

    def get_current_date_file_name(self):
        ts = datetime.now().strftime("%Y-%m-%d")
        return "{}/{}.txt".format(self.data_path, ts)

    @staticmethod
    def save_data(file_name, news_headers):
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

            for header_txt in news_headers:
                if get_header_hash(header_txt) not in data_hashes:
                    f.write('{}\n'.format(header_txt))

    @staticmethod
    def fetch_page_headers(page_html):
        soup = BeautifulSoup(page_html, 'html5lib')
        headers_mobile = list(
            map(
                lambda a: a.string,
                soup.find_all('span', {'class': 'helpers_show_mobile-small'})
            )
        )
        headers_body = list(
            map(
                lambda a: a.find('span', {'class': 'text-i'}).string,
                soup.find_all('a', {'class': 'b-teasers-2__teaser-i'})
            )
        )
        headers_list_full = headers_body + headers_mobile
        headers_filtered = HeadGrab.get_filtered_headers(headers_list_full)

        logging.info('found {}'.format(len(headers_filtered)))

        return headers_filtered

    @staticmethod
    def get_filtered_headers(headers):
        filtered = []
        for header in headers:
            if len(header.split(' ')) > MIN_PHRASE_WORDS:
                clear_header = header.replace('»', '').replace('«', '')
                filtered.append(clear_header)
        return filtered

def grab():
    data_path = os.environ.get('DATA_PATH')
    if not data_path:
        raise Exception("Please setup path to storing data [data_path] var")
    hg = HeadGrab(data_path, TARGET_URL)
    hg.run()


if __name__ == "__main__":
    grab()
