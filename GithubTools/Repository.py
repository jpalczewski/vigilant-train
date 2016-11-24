import base64
import config
import requests
import sys

class RepositoryException(Exception):
    pass


def record_print(filepath, filecontent):
    print(filepath,"\n", filecontent)

class Repository(object):


    def __init__(self, url):
        try:
            self.repo_url = url

            self.last_commit = requests.get(
                self.repo_url + "/commits",
                auth=(config.user, config.oauth)
            ).json()[0]['sha']

            self.file_tree = requests.get(
                self.repo_url + "/git/trees/" + self.last_commit + "?recursive=1",
                auth=(config.user, config.oauth)
            ).json()

        except Exception as e:
            raise RepositoryException(e)

    def review_all_files(self, func):
        """Print all files from repo_url."""

        for f in self.file_tree['tree']:
            print("---[CUT HERE]---")
            filepath = f['path']

            try:
                blob = requests.get(f['url'],
                                    auth=(config.user, config.oauth)).json()

                # it's a folder
                if 'content' not in blob:
                    continue
                file_content = blob['content'].replace('\n', '')
                decoded_content = base64.b64decode(file_content).decode("utf-8")
                func(filepath, decoded_content)
            except UnicodeDecodeError:
                print("[!] Unicode decoding error!", file=sys.stderr)
                continue #It just cannot be decoded - PNG or other file.
            except Exception as e:
                print("[!] Exception: ", e)
                pass
        print("---[CUT HERE]---")

    def print_all_files(self):
        self.review_all_files(record_print)


