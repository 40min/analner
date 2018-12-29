import os
import logging
import glob
import markovify

from analner.utils.dropbox_sync import DropboxSync

READY_TO_USE_MODEL_FILE_NAME = 'news.json'
MAX_ATTEMPTS_TO_GET_PHRASE = 100


class FunMaker:

    dropbox_syncer = None

    def __init__(self, data_path, dropbox_token=None):
        self.data_path = data_path
        self.dropbox_token = dropbox_token
        self._text_model = self._get_model()
        self.sync_with_dropbox()

    def sync_with_dropbox(self):
        if not self.dropbox_token:
            return
        if not self.dropbox_syncer:
            self.dropbox_syncer = DropboxSync(self.dropbox_token)
        remote_path = self.data_path.strip('.')
        synced = self.dropbox_syncer.sync_with_dropbox(self.data_path, remote_path)
        if synced:
            self.reload_model_from_txt()

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
            try:
                s = self._text_model.make_sentence_with_start(with_phrase, strict=False)
                if s:
                    return s
            except KeyError:
                pass
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
            with open(model_file, 'w', encoding='utf-8') as saving:
                saving.write(text_model.to_json())
        return text_model

    def _get_model_from_text(self):
        news_text = ''
        news_file_path_pattern = '{}/*.txt' . format(self.data_path)
        files = glob.glob(news_file_path_pattern)
        for file in files:
            with open(file, encoding='utf-8') as f:
                text = f.read()
                news_text = f'{news_text}\n{text}'
        news_model = markovify.NewlineText(news_text)

        return news_model

    @staticmethod
    def _load_saved_model(model_file):
        text_model = None
        if os.path.isfile(model_file):
            try:
                with open(model_file, 'r', encoding='utf-8') as saved:
                    text_model = markovify.NewlineText.from_json(saved.read())
            except ValueError:
                logging.info("No JSON saved data found")
        return text_model


if __name__ == "__main__":
    dropbox_token = os.environ.get('DROPBOX_TOKEN')
    data_path = os.environ.get('DATA_PATH')
    if not data_path:
        raise Exception("Please setup path to storing data [data_path] var")

    print("Enter phrase to do 'with' or just leave empty:")
    fm = FunMaker(data_path, dropbox_token)
    while True:
        phrase = 'No results'
        with_phrase = str(input())
        if with_phrase:
            phrase = fm.make_phrases_with(with_phrase) or phrase
        else:
            phrases = fm.make_phrases()
            phrase = phrases[0] if phrases else phrase

        print(phrase)



