import pymongo
from collections import Counter
from multiprocessing import Pool, TimeoutError

def generate_simple_stat(f):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    files = client.files.files

    #calculate
    cleaned = f['content'].replace(".", "").replace("$", "").replace("\0", "")
    c = Counter(cleaned)
    simple_stat = {'char_occurrences': {}, 'token_occurrences': {}}
    for char, count in c.items():
        simple_stat['char_occurrences'][char] = count

    allTokens = cleaned.split()
    uniqueTokens = set(allTokens)
    for t in uniqueTokens:
        simple_stat['token_occurrences'][t] = allTokens.count(t)
    if 'stats' not in f.keys():
        f['stats'] = {}
    f['stats']['simple'] = simple_stat
    files.replace_one({'_id': f['_id']}, f)


client = pymongo.MongoClient('mongodb://localhost:27017/')
files = client.files.files

allFiles = files.find({})
listAllFiles = list(allFiles)


with Pool(processes=4) as pool:
    pool.map(generate_simple_stat, listAllFiles)


