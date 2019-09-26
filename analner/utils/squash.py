import os
import re
import logging
from datetime import datetime
from collections import defaultdict
from analner.utils.dropbox_sync import DropboxSync


logger = logging.getLogger(__name__)


class SquashError(Exception):
    pass


class Squasher:

    def __init__(self, data_path: str, db_sync: DropboxSync):
        self._data_path = data_path
        self._remote_path = data_path.strip('.')
        self.current_year = str(datetime.utcnow().year)
        self.current_month = str(datetime.utcnow().month).rjust(2, '0')
        self._db_sync = db_sync

    def squash_by(self, date_period_pattern, current_date_parts):
        logger.info("Logging against %s", "_".join(current_date_parts))
        files_to_delete = list()
        squashed_periods = defaultdict(str)
        for file_name in os.listdir(self._data_path):
            if date_period_pattern.match(file_name):
                date_parts = file_name.split("-")
                if len(date_parts) < 2:
                    raise SquashError("Can't squash files with less than 2 sections. Sections must be delimited with _")
                if current_date_parts != date_parts[:-1]:
                    files_to_delete.append(file_name)
                    result_file = f"{'-'.join(date_parts[:-1])}.txt"
                    with open(os.path.join(self._data_path, file_name), 'r', encoding='utf-8') as fd:
                        squashed_periods[result_file] += fd.read()

        for file_name, data in squashed_periods.items():
            local_file_path = os.path.join(self._data_path, file_name)
            with open(local_file_path, 'w', encoding='utf-8') as fd:
                fd.write(data)
            remote_file_path = os.path.join(self._remote_path, file_name)
            self._db_sync.upload_file(local_file_path, remote_file_path)
        logger.info("Squashed to %d files", len(squashed_periods))

        for file_name in files_to_delete:
            remote_file_path = os.path.join(self._remote_path, file_name)
            self._db_sync.delete_file(remote_file_path)
            local_file_path = os.path.join(self._data_path, file_name)
            os.remove(local_file_path)
        logger.info("Deleted %d files", len(files_to_delete))

    def run(self):
        day_pattern = re.compile("^\d{4}-\d{2}-\d{2}\.txt$")
        self.squash_by(day_pattern, [self.current_year, self.current_month])

        month_pattern = re.compile("^\d{4}-\d{2}\.txt$")
        self.squash_by(month_pattern, [self.current_year])


if __name__ == "__main__":
    data_path = os.environ.get('DATA_PATH')
    if not data_path:
        raise Exception("Please setup path to storing data [data_path] var")

    token = os.environ.get('DROPBOX_TOKEN')
    if not token:
        raise Exception("Please add DROPBOX_TOKEN to environment vars")
    db_sync = DropboxSync(token)

    squasher = Squasher(data_path, db_sync)
    squasher.run()
