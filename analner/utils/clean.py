import os

MIN_LENGTH = 5


class Cleaner:

    was_count = 0
    deleted_count = 0

    def __init__(self, target_dir, min_length):
        self.target_dir = target_dir
        self.min_length = min_length

    def clean_short(self):
        for file in os.listdir(self.target_dir):
            current_headers = list()
            current_shorts = list()
            need_deletion = False
            with open(os.path.join(self.target_dir, file), 'r') as fd:
                data = fd.read()
                for h in data.split('\n'):
                    h_len = len(h.split(' '))
                    if h_len < self.min_length:
                        need_deletion = True
                        current_shorts.append(h)
                        self.deleted_count += 1
                    else:
                        current_headers.append(h)
                    self.was_count += 1

            if need_deletion:
                self.rewrite_file(current_headers, file)

    def clean_doubles(self):
        headers = dict()
        for file in os.listdir(self.target_dir):
            current_headers = list()
            current_doubles = list()
            need_deletion = False
            with open(os.path.join(self.target_dir, file), 'r') as fd:
                data = fd.read()
                for h in data.split('\n'):
                    if h in headers:
                        headers[h] = headers[h] + 1
                        need_deletion = True
                        current_doubles.append(h)
                        self.deleted_count += 1
                    else:
                        headers[h] = 1
                        current_headers.append(h)
                    self.was_count += 1

            if need_deletion:
                self.rewrite_file(current_headers, file)

    def rewrite_file(self, current_headers, file):
        print(f'deleted from {file}')
        headers_to_write = '\n'.join(current_headers)
        with open(os.path.join(self.target_dir, file), 'w') as fd:
            fd.write(headers_to_write)

    def print_results(self):
        print(f'Headers was {self.was_count}')
        print(f'Headers deleted {self.deleted_count}')

    def reset_results(self):
        self.deleted_count = 0
        self.was_count = 0


if __name__ == "__main__":
    cleaner = Cleaner('./grabbed_headers', MIN_LENGTH)
    # cleaner.clean_short()
    # cleaner.print_results()
    # cleaner.reset_results()
    cleaner.clean_doubles()
    cleaner.print_results()
