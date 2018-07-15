import os
import re
import logging
import glob
import markovify
import spacy

from head_grab import grabbed_headers_path

nlp = spacy.load("xx")
current_dir = os.path.dirname(os.path.realpath(__file__))
saved_model_file_path = '{}/model.json' . format(current_dir)


class SpacyNewLinedText(markovify.NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def get_model_from_txt():
    news_text = ''
    news_file_path_pattern = f'{grabbed_headers_path}/*.txt'
    files = glob.glob(news_file_path_pattern)
    for file in files:
        with open(file) as f:
            text = f.read()
            text = re.sub('(«|»)', '', text)
            news_text = f'{news_text}\n{text}'

    news_model = SpacyNewLinedText(news_text)
    return news_model


def get_model_from_json(model_file):
    try:
        with open(model_file, 'r') as saved:
            news_model = SpacyNewLinedText.from_json(saved.read())
    except ValueError:
        logging.info("No JSON saved data found")
    return news_model


def make_news(news_count=1):
    if os.path.isfile(saved_model_file_path):
        text_model = get_model_from_json(saved_model_file_path)
    else:
        text_model = get_model_from_txt()
        with open(saved_model_file_path, 'w') as saving:
            saving.write(text_model.to_json())

    for i in range(news_count):
        s = text_model.make_sentence()
        if s:
            print(s)


if __name__ == "__main__":
    make_news(10)
