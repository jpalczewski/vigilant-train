from GithubTools.GithubScraper import GithubScraper, GithubScraperException
from GithubTools.Repository import Repository, RepositoryException
from DeadRatioSwitch import DeadRatioSwitch
from FileDriver import FileDriver
import datetime
import threading
import config
import sys
import click
import multiprocessing
import requests



@click.group()
def cli():
    pass


@cli.command(name="stats")
def github_stats():
    try:
        gs = GithubScraper()
        limit, epoch, date = gs.get_reset_response()

        print("X-RateLimit-Remaining:", limit)
        print("X-RateLimit-Reset:", date)


        dt = datetime.datetime.fromtimestamp(float(epoch)) - datetime.datetime.now()
        print("Remaining time:",  dt.seconds//60, " min,", dt.seconds%60, " secs")
    except GithubScraperException:
        sys.exit(1)

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


def mtsave_worker(q, gs, fd):
    remaining, boring, notuseful = gs.get_reset_response()
    print("[MTW] Entered thread")
    while remaining !=0 or not q.empty():
        repo = q.get()
        print("[MTW] Loop,", repo.repo_url, " remaining ", remaining)
        repo.review_all_files(fd.save_file)
        remaining = gs.get_reset_response()[0]
    sys.exit(1)

@cli.command(name="mtsave")
@click.option('--number', '-n', default=10)
@click.option('--threads', '-j', default=5)
def mtsave(number, threads):
    print("hello, multithreaded world")
    t = []
    try:
        t = threading.Thread(target=DeadRatioSwitch,args=(0,))
        t.start()
    except Exception as e:
        print("????? exception setting DRS:", e)
        pass

    try:
        gs = GithubScraper()
        fd = FileDriver()
        pool = multiprocessing.Pool(processes=threads)
        m = multiprocessing.Manager()
        q = m.Queue()
        repos = gs.get_random_repo_range(number)
        results = []

        for r in repos:
            q.put(r)
        for i in range(threads):
            results.append(pool.apply_async(mtsave_worker, args=(q, gs, fd)))

        print("After applying")

        for j in results:
            j.get()

        pool.close()
        pool.join()


    except (GithubScraperException, RepositoryException):
        sys.exit(1)

if __name__ == "__main__":
    cli()


