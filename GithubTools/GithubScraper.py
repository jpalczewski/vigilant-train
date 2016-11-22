"""Implement GithubScraper class."""
import random
import requests
import time


class GithubScraper(object):
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
        return "foo"
