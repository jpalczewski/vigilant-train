import base64
import config
import requests
import sys

class RepositoryException(Exception):
    pass


def record_print(file_path, file_content, repo_url):
    print(file_path)

class Repository(object):


    def __init__(self, url):

        self.repo_url = url

    def __lazy_init(self):
        try:

            self.last_commit = requests.get(
                self.repo_url + "/commits",
                auth=(config.user, config.oauth)
            ).json()[0]['sha']

            self.file_tree = requests.get(
                self.repo_url + "/git/trees/" + self.last_commit + "?recursive=1",
                auth=(config.user, config.oauth)
            ).json()


        except KeyError:
            # empty repo
            self.last_commit = None
            self.file_tree = None
        except Exception as e:
            print("[!] Repository.__init__ exception:", e)
            raise RepositoryException(e)

    def review_all_files(self, func):
        """Run func for all files from repo_url."""
        self.__lazy_init()

        for f in self.file_tree['tree']:
            filepath = f['path']

            try:
                blob = requests.get(f['url'],
                                    auth=(config.user, config.oauth)).json()

                # it's a folder
                if 'content' not in blob:
                    continue
                file_content = blob['content'].replace('\n', '')
                decoded_content = base64.b64decode(file_content)
                func(filepath, decoded_content, self.repo_url)
            except UnicodeDecodeError:
                #It isn't
                print("[!] Unicode decoding error!", file=sys.stderr)
                continue #It just cannot be decoded - PNG or other file.
            except Exception as e:
                print("[!] Exception: ", e, file=sys.stderr)
                pass

    def print_all_files(self):
        self.review_all_files(record_print)


