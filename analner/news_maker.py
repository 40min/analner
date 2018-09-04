import os
import logging
import glob
import markovify
import spacy

nlp = spacy.load("xx")


class SpacyNewLinedText(markovify.NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


class FunMaker:

    def __init__(self, data_path):
        self.data_path = data_path

    def get_news_model(self):
        news_text = ''
        news_file_path_pattern = '{}/*.txt' . format(self.data_path)
        files = glob.glob(news_file_path_pattern)
        for file in files:
            with open(file) as f:
                text = f.read()
                news_text = f'{news_text}\n{text}'
        news_model = SpacyNewLinedText(news_text)

        return news_model

    def make_fun(self):
        result = []
        model_file = '{}/news.json' . format(self.data_path)
        if os.path.isfile(model_file):
            try:
                with open(model_file, 'r') as saved:
                    text_model = SpacyNewLinedText.from_json(saved.read())
            except ValueError:
                logging.info("No JSON saved data found")
        else:
            text_model = self.get_news_model()
            with open(model_file, 'w') as saving:
                saving.write(text_model.to_json())

        for i in range(5):
            s = text_model.make_sentence()
            if s:
                result.append(s)
        return result


if __name__ == "__main__":
    data_path = os.environ.get('DATA_PATH')
    if not data_path:
        raise Exception("Please setup path to storing data [data_path] var")

    fm = FunMaker(data_path)
    print(fm.make_fun())
