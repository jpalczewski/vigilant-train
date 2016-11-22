from GithubTools.GithubScraper import GithubScraper
import sys

if __name__ == "__main__":
    print("Hello, world")

    gs = ""
    try:
        gs = GithubScraper()
    except EnvironmentError:
        sys.exit(1)

    gs.get_random_repo()
