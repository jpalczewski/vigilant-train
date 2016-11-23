from GithubTools.GithubScraper import GithubScraper
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
    url = gs.get_random_repo()
    print("Selected url:", url)
    gs.print_all_files(url)


if __name__ == "__main__":
    cli()
