from GithubTools.GithubScraper import GithubScraper
from GithubTools.Repository import Repository, RepositoryException
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
    print(r.headers)

@cli.command(name="print")
def print_all():
    print("Hello, world")
    gs = ""
    try:
        gs = GithubScraper()
    except EnvironmentError:
        sys.exit(1)
    repo = gs.get_random_repo()

    print("Selected url:", repo.repo_url)

    repo.print_all_files()


if __name__ == "__main__":
    cli()
