import os
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


def get_news_model():
    news_text = ''
    news_file_path_pattern = f'{data_path}/*.txt'
    files = glob.glob(news_file_path_pattern)
    for file in files:
        with open(file) as f:
            text = f.read()
            news_text = f'{news_text}\n{text}'
    news_model = SpacyNewLinedText(news_text)

    return news_model


def make_fun():
    model_file = './news.json'
    if os.path.isfile(model_file):
        try:
            with open(model_file, 'r') as saved:
                text_model = SpacyNewLinedText.from_json(saved.read())
        except ValueError:
            logging.info("No JSON saved data found")
    else:
        text_model = get_news_model()
        with open(model_file, 'w') as saving:
            saving.write(text_model.to_json())

    for i in range(1):
        s = text_model.make_sentence()
        if s:
            print(s)


if __name__ == "__main__":
    make_fun()
