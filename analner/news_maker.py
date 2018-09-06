import os
import logging
import glob
import markovify
import spacy

READY_TO_USE_MODEL_FILE_NAME = 'news.json'
MAX_ATTEMPTS_TO_GET_PHRASE = 100

try:
    nlp = spacy.load("xx")
except OSError as e:
    from spacy.cli import download
    download('xx')


class SpacyNewLinedText(markovify.NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


class FunMaker:

    def __init__(self, data_path):
        self.data_path = data_path
        self._text_model = self._get_model()

    def make_phrases(self, phrases_needed=1):
        result = []
        attempts = MAX_ATTEMPTS_TO_GET_PHRASE
        while attempts:
            attempts -= 1
            s = self._text_model.make_sentence()
            if s and s not in result:
                result.append(s)
                if len(result) == phrases_needed:
                    return result
                attempts = MAX_ATTEMPTS_TO_GET_PHRASE
        return result

    def make_phrases_with(self, with_phrase):
        with_parts = with_phrase.split(' ')[0:2]
        if len(with_parts) != 2:
            return None
        with_phrase = ' '.join(with_parts)
        attempts = MAX_ATTEMPTS_TO_GET_PHRASE
        while attempts:
            attempts -= 1
            s = self._text_model.make_sentence_with_start(with_phrase, strict=False)
            if s:
                return s
        return None

    def reload_model_from_txt(self):
        model_file = self._get_model_full_path()
        if os.path.isfile(model_file):
            os.remove(model_file)
        self._text_model = self._get_model()

    def _get_model_full_path(self):
        return '{}/{}'.format(self.data_path, READY_TO_USE_MODEL_FILE_NAME)

    def _get_model(self):
        model_file = self._get_model_full_path()
        text_model = self._load_saved_model(model_file)
        if not text_model:
            text_model = self._get_model_from_text()
            with open(model_file, 'w') as saving:
                saving.write(text_model.to_json())
        return text_model

    def _get_model_from_text(self):
        news_text = ''
        news_file_path_pattern = '{}/*.txt' . format(self.data_path)
        files = glob.glob(news_file_path_pattern)
        for file in files:
            with open(file) as f:
                text = f.read()
                news_text = f'{news_text}\n{text}'
        news_model = SpacyNewLinedText(news_text)

        return news_model

    @staticmethod
    def _load_saved_model(model_file):
        text_model = None
        if os.path.isfile(model_file):
            try:
                with open(model_file, 'r') as saved:
                    text_model = SpacyNewLinedText.from_json(saved.read())
            except ValueError:
                logging.info("No JSON saved data found")
        return text_model


if __name__ == "__main__":
    data_path = os.environ.get('DATA_PATH')
    if not data_path:
        raise Exception("Please setup path to storing data [data_path] var")

    fm = FunMaker(data_path)
    fm.reload_model_from_txt()
    for f in fm.make_phrases(5):
        print(f)

    print(fm.make_phrases_with('список'))
