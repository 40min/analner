import os
import re
import logging
import glob
import markovify
import spacy

from head_grab import grabbed_headers_path

nlp = spacy.load("xx")


class SpacyNewLinedText(markovify.NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


class NewsMaker:

    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.saved_model_file_path = '{}/model.json'.format(current_dir)

    @staticmethod
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

    @staticmethod
    def get_model_from_json(model_file):
        try:
            with open(model_file, 'r') as saved:
                news_model = SpacyNewLinedText.from_json(saved.read())
        except ValueError:
            logging.info("No JSON saved data found")
        return news_model

    def make_news(self, news_count=1, force_get_from_text=False):
        if not force_get_from_text and os.path.isfile(self.saved_model_file_path):
            text_model = self.get_model_from_json(self.saved_model_file_path)
        else:
            text_model = self.get_model_from_txt()
            with open(self.saved_model_file_path, 'w') as saving:
                saving.write(text_model.to_json())

        news = []
        for i in range(news_count):
            s = text_model.make_sentence()
            if s:
                news.append(s)
        return news


if __name__ == "__main__":
    news = NewsMaker().make_news(10)
    for n in news:
        print(n)
