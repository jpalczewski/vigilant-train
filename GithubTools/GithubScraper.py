"""Implement GithubScraper class."""
import base64
import random
import requests
import time

MAX_REPOSITORY_ID = 70000000

user = "jpalczewski"
oauth = "none"

class GithubScraper:
    """Find random repository."""

    def __init__(self) -> object:
        """Constructor."""

        # We should be confident about randomness
        seed = int(time.time())
        random.seed(seed)

        # We might die whether net or github isn't available.
        try:
            requests.get('http://github.com', timeout=1)

        except (requests.ConnectionError, requests.Timeout) as e:
            print("[!] Unrecoverable exception: ", e)
            raise EnvironmentError

    def get_random_repo(self):
        """Return random repository as string."""
        dice = random.randint(1, MAX_REPOSITORY_ID)

        repo_list = requests.get("https://api.github.com/repositories?since=" + str(dice), auth=(user, oauth)).json()
        repo_url = repo_list[0]['url']

        last_commit = requests.get(repo_url + "/commits", auth=(user, oauth)).json()[0]['sha']

        file_tree = requests.get(repo_url + "/git/trees/" + last_commit + "?recursive=1",auth=(user, oauth)).json()

        for f in file_tree['tree']:
            print("---[CUT HERE]---")
            blob = requests.get(f['url'], auth=(user, oauth)).json()
            try:
                file_content = blob['content'].replace('\n', '')
                print(base64.b64decode(file_content).decode("utf-8"))
            except:
                pass

        print("---[CUT HERE]---")
        return "foo"

