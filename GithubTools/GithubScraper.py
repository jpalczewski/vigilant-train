"""Implement GithubScraper class."""
import base64
import config
import random
import requests
import time
from GithubTools.Repository import Repository


MAX_REPOSITORY_ID = 70000000

class GithubScraperException(Exception):
    pass


class GithubScraper(object):
    """Find random repository."""

    def __init__(self):
        """Constructor."""
        # We should be confident about randomness
        seed = int(time.time())
        random.seed(seed)

        # We might die whether net or github isn't available.
        self.__network_check()

    @staticmethod
    def __network_check():
        try:
            requests.get('http://github.com', timeout=1)

        except (requests.ConnectionError, requests.Timeout) as e:
            print("[!] Unrecoverable exception: ", e)
            raise GithubScraperException(e)

    def get_random_repo(self):
        """Return random repository as string.

        Algorithm:
        1. Runs query for repository with random ID.
        2. Gets first one.
        3. Returns its url.
        """
        dice = random.randint(1, MAX_REPOSITORY_ID)
        repositories_url = "https://api.github.com/repositories?since="+ str(dice)

        repo_list = requests.get(
            repositories_url,
            auth=(config.user, config.oauth)
        ).json()
        repo_url = repo_list[0]['url']

        return Repository(repo_url)
