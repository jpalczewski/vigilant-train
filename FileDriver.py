import hashlib
import os

class FileDriverException(Exception):
    pass


class FileDriver(object):

    def __init__(self, directory='./data'):
        self.directory = directory


    def save_file(self, file_name, file_content, repo_url):
        (root, ext) = os.path.splitext(file_name)

        ext = ext.replace('.', '')
        if ext == '':
            return

        hashed = hashlib.md5((file_name+repo_url).encode('utf-8')).hexdigest()

        suggested_path = "{0}/Incoming/{1}/{2}.{1}".format(self.directory, ext, hashed, ext)
        suggested_folder = os.path.dirname(suggested_path)
        if not os.path.exists(suggested_folder):
            os.makedirs(suggested_folder)

        with open(suggested_path, 'w') as f:
            f.write(file_content)
