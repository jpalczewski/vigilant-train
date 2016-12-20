import threading
import os
from GithubTools.GithubScraper import GithubScraper, GithubScraperException

time_limit = 1.0
gs = GithubScraper()
min_ratio = 0

def DeadRatioCheck():
    actual_ratio = gs.get_reset_response()[0]
    print("[DRS] fired, {now}/{limit}".format(now=actual_ratio, limit=min_ratio))
    if actual_ratio <= min_ratio:
        os._exit(0x1337)

def DeadRatioSwitch(minimum):
    min_ratio = minimum
    while True:
        t = threading.Timer(time_limit, DeadRatioCheck)
        t.start()
        t.join()