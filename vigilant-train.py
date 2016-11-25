from GithubTools.GithubScraper import GithubScraper, GithubScraperException
from GithubTools.Repository import Repository, RepositoryException
from FileDriver import FileDriver
import config
import sys
import click
import requests



@click.group()
def cli():
    pass


@cli.command(name="stats")
def github_stats():
    r = requests.get("https://api.github.com/user", auth=(config.user, config.oauth))
    print("X-RateLimit-Remaining:",r.headers['X-RateLimit-Remaining'])
    rate_reset = r.headers['X-RateLimit-Reset']
    
    print(r.headers)

@cli.command(name="print")
def print_all():
    print("Hello, world")
    gs = ""
    try:
        gs = GithubScraper()
        repo = gs.get_random_repo()
        print("Selected url:", repo.repo_url)
        repo.print_all_files()

    except (GithubScraperException, RepositoryException):
        sys.exit(1)

@cli.command(name="save")
def save_all():
    print("Hello, world")
    gs = ""
    try:
        gs = GithubScraper()
        fd = FileDriver()

        repo = gs.get_random_repo()
        print("Selected url:", repo.repo_url)
        repo.review_all_files(fd.save_file)

    except (GithubScraperException, RepositoryException):
        sys.exit(1)


if __name__ == "__main__":
    cli()
