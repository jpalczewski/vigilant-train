"""Implement GithubScraper class."""
import base64
import config
import random
import requests
import time
import datetime
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
            requests.get('http://github.com', timeout=5)

        except (requests.ConnectionError, requests.Timeout) as e:
            print("[!] Unrecoverable exception: ", e)
            raise GithubScraperException(e)

    def get_random_repo_range(self, range=None):
        """Return random repository as Repository object.

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
        if range is not None:
            repo_list = repo_list[0:range]
        repo_range =  [Repository(x['url']) for x in repo_list]

        return repo_range

    def get_random_repo(self):
        return self.get_random_repo_range(1)[0]

    def get_reset_response(self):
        r = requests.get("https://api.github.com/user", auth=(config.user, config.oauth))
        remaining = r.headers['X-RateLimit-Remaining']

        rate_reset = r.headers['X-RateLimit-Reset']
        rate_reset_date = datetime.datetime.fromtimestamp(int(rate_reset) / 1.0).strftime('%c')

        return remaining, rate_reset, rate_reset_date

