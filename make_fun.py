import markovify

from pathlib import Path

from head_grab import get_current_date_file_name
from head_grab import fetch_fresh_headers


def load_fun(current_file_name):
    my_file = Path(current_file_name)
    if my_file.is_file():
        print(f'Load headers from file {current_file_name}:')
        with open(current_file_name) as f:
            text = f.read()
            return text
    return ''


def get_today_headers():
    current_file_name = get_current_date_file_name()
    text = load_fun(current_file_name)
    if not text:
        headers_list = fetch_fresh_headers(current_file_name)
        text = '. \n'.join(headers_list)

    return text


def make_fun(text=''):
    with open("./test_data/corpus2.txt") as f:
        text2 = f.read()

    text_model = markovify.Text(text + text2)

    for i in range(5):
        print(text_model.make_sentence())


headers = get_today_headers()
make_fun(headers)
