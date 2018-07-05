import glob
import markovify

from head_grab import grabbed_headers_path


def load_news():
    news_text = ''
    news_file_path_pattern = f'{grabbed_headers_path}/*.txt'
    files = glob.glob(news_file_path_pattern)
    for file in files:
        with open(file) as f:
            text = f.read()
            news_text = f'{news_text}\n{text}'
    return news_text


def make_fun(text=''):
    text_model = markovify.NewlineText(text)

    print('---------------------------------------------------')
    for i in range(5):
        s = text_model.make_sentence(tries=100)
        if s:
            print(s)

    print('---------------------------------------------------')
    for i in range(3):
        s = text_model.make_short_sentence(140)
        if s:
            print(s)


if __name__ == "__main__":
    news = load_news()
    make_fun(news)
