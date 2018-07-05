from bs4 import BeautifulSoup

from head_grab import grabbed_headers_path
from head_grab import request_page
from head_grab import fetch_page_headers
from head_grab import save_data

arch_base = 'https://web.archive.org/'
arch_start_year_url = 'https://web.archive.org/web/20170601000000*/onliner.by'
arch_url = 'https://web.archive.org/web/20161130113014/onliner.by'
DAYS_TO_GRAB = 60
grabbed_days = 0

# stopping here: fetch of list from calendar not working, try to fetch from json loaded to page

def get_file_name_from_url(url):
    year = url[28:32]
    month = url[32:34]
    day = url[34:36]

    return f"{grabbed_headers_path}/{year}-{month}-{day}.txt"


def get_next_link(page_html):
    soup = BeautifulSoup(page_html, 'html5lib')
    img_back = soup.find('img', {'alt': 'Previous capture'})
    if img_back:
        return img_back.parent['href']
    return None


def get_arch_links():
    res_links = []
    arc_page = request_page(arch_start_year_url)
    soup = BeautifulSoup(arc_page, 'html5lib')
    link_divs = soup.find_all('div', {'class': 'month-day'})
    for l in link_divs:
        res_links.append(l.find('a')['href'])


if __name__ == "__main__":
    # links = get_arch_links()
    # a = 1
    while arch_url and grabbed_days < DAYS_TO_GRAB:
        print(f'request news from {arch_url}')
        page = request_page(arch_url)
        news_headers = fetch_page_headers(page)
        news_file_name = get_file_name_from_url(arch_url)
        save_data(news_file_name, news_headers)
        arch_url = get_next_link(page)
