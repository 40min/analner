import os
import dropbox
from dropbox.files import FolderMetadata


class DropboxSync:
    """ Dropbox sync class """

    def __init__(self, token):
        """
        :param token: str
        """
        self.dbx = dropbox.Dropbox(token)
        self.dbx.users_get_current_account()

    def get_target_dir_content(self, path=''):
        """
        Return list of entities (folders/files) in remote dir
        :param path: str
        :return: []
        """
        return self.dbx.files_list_folder(path).entries

    def upload_file(self, local_file_path, remote_file_path=None, overwrite=False):
        """
        Upload file to dropbox

        :param local_file_path: str
        :param remote_file_path: str
        :param overwrite: bool
        :return: Object
        """
        remote_file_path = local_file_path if remote_file_path is None else remote_file_path
        mode = dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add
        with open(local_file_path, 'r', encoding='utf-8') as fd:
            content = fd.read()
        content = content.encode()
        try:
            res = self.dbx.files_upload(content, remote_file_path, mode, mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
        return res

    def get_file_content(self, path):
        """
        Return content of remote file (as string)
        :param path: str full path on remote with starting /
        :return: str
        """
        try:
            _, response = self.dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None

        return response.content.decode()

    def sync_with_dropbox(self, local_dir, remote_dir, recursive=False):
        """
        One directional sync with dropbox (all new in dropbox will be added)
        added/deleted locally won't affect remote
        :param local_dir: str
        :param remote_dir: str
        :param recursive: bool
        :return: int
        """
        synced_count = 0
        remote_content = self.get_target_dir_content(remote_dir)
        for entry in remote_content:
            local_file = os.path.join(local_dir, entry.name)
            if isinstance(entry, FolderMetadata):
                if not recursive:
                    continue
                new_remote_dir = entry.path_display
                new_local_dir = local_file
                if not os.path.isdir(new_local_dir):
                    os.mkdir(new_local_dir)
                self.sync_with_dropbox(new_local_dir, new_remote_dir, recursive)
            elif not os.path.exists(local_file):
                content = self.get_file_content(entry.path_display)
                with open(local_file, 'w', encoding='utf-8') as fd:
                    fd.write(content)
                synced_count += 1

        return synced_count


if __name__ == "__main__":
    local_dir = os.environ.get('DATA_PATH', './grabbed_headers')
    remote_dir = os.environ.get('REMOTE_DATA_PATH', '')
    token = os.environ.get('DROPBOX_TOKEN')

    db_sync = DropboxSync(token)
    db_sync.sync_with_dropbox(local_dir, remote_dir='', recursive=True)
